# api_automation_project/tests/test_price_calculation.py
import pytest
import json
import time  # Added to handle backend calculation delay
from api_automation_project.api_clients.ecom_api_client import EcomApiClient


@pytest.mark.parametrize(
    "target_product_id, expected_total_offered_price, sub_item_id_to_fix, payload_to_fix",
    [
        # (Product to Search, Expected Total Price, Sub-Item to Update, New Price Data)
        (
                "ol_micro_plus_3_a",
                7190,
                "MlqJBm",
                {"offeredPrice": 2430, "mrp": 5400}
        )
    ]
)
def test_verify_and_fix_price_calculation(api_context, target_product_id, expected_total_offered_price,
                                          sub_item_id_to_fix, payload_to_fix):
    ecom_api = EcomApiClient(api_context)

    print(f"\n\n{'=' * 70}")
    print(f"SMART AUTOMATION STARTED FOR: {target_product_id}")
    print(f"{'=' * 70}")

    # --- Helper Function: Extract current price from all-v2 API ---
    def get_product_details_from_v2(product_id):
        all_products_response = ecom_api.get_all_products_v2()
        all_products_list = []
        if isinstance(all_products_response, list):
            all_products_list = all_products_response
        elif isinstance(all_products_response, dict):
            for key, value in all_products_response.items():
                if isinstance(value, list):
                    all_products_list = value
                    break

        for product in all_products_list:
            if isinstance(product, dict):
                if product.get('productId') == product_id or product.get('name') == product_id or product.get(
                        'id') == product_id:
                    return product
        return None

    # ---------------------------------------------------------
    # STEP 1: Search product in all-v2 API & check current price
    # ---------------------------------------------------------
    print("\n STEP 1: SEARCHING PRODUCT IN 'ALL-V2' API...")
    current_product_data = get_product_details_from_v2(target_product_id)

    assert current_product_data is not None, f"Product '{target_product_id}' not found in all-v2 API!"

    current_offered_price = current_product_data.get('offeredPrice')

    print(f"   -> Expected Total Offered Price : ₹{expected_total_offered_price}")
    print(f"   -> Current Actual Offered Price : ₹{current_offered_price}")

    # ---------------------------------------------------------
    # STEP 2: Conditional Update (Fix price if incorrect)
    # ---------------------------------------------------------
    if current_offered_price == expected_total_offered_price:
        print("\n PRICE IS ALREADY CORRECT! No update needed.")
    else:
        print("\n ALERT: INCORRECT OFFERED PRICE DETECTED!")
        print(f"      Difference: Expected ₹{expected_total_offered_price}, but found ₹{current_offered_price}.")

        print(f"\nSTEP 2: TRIGGERING PUT API TO FIX PRICE FOR SUB-ITEM '{sub_item_id_to_fix}'...")
        print(f"   -> Passing Payload: {json.dumps(payload_to_fix)}")

        # Update the sub-item price
        update_response = ecom_api.update_sub_item_price(sub_item_id_to_fix, payload_to_fix)
        assert update_response.ok, f"Failed to update price! Status: {update_response.status}"
        print("Sub-item price updated successfully!")

        # Wait for backend calculation to reflect
        print("Waiting 2 seconds for backend calculation to refresh...")
        time.sleep(2)

        # ---------------------------------------------------------
        # STEP 3: Re-verify calculation after update
        # ---------------------------------------------------------
        print("\nSTEP 3: RE-CHECKING 'ALL-V2' API AFTER UPDATE...")
        updated_product_data = get_product_details_from_v2(target_product_id)
        new_offered_price = updated_product_data.get('offeredPrice')

        print(f"   -> New Calculated Offered Price: ₹{new_offered_price}")

        assert new_offered_price == expected_total_offered_price, \
            f"PRICE FIX FAILED! Even after update, price is ₹{new_offered_price} (Expected ₹{expected_total_offered_price})"
        print(" UPDATE SUCCESSFUL! Calculation is now correct.")

    # ---------------------------------------------------------
    # STEP 4: Final Match/Mismatch Check
    # ---------------------------------------------------------
    print(f"\nSTEP 4: CHECKING FINAL MATCH/MISMATCH STATUS")
    match_mismatch_data = ecom_api.get_mismatched_products()

    matched_list = match_mismatch_data.get('matched', [])
    mismatched_list = match_mismatch_data.get('mismatched', [])

    if target_product_id in matched_list:
        print(f"FINAL RESULT: '{target_product_id}' IS NOW IN THE 'MATCHED' LIST!")
    else:
        mismatched_details = next((item for item in mismatched_list if target_product_id in item), "No details found.")
        print(f"WARNING: '{target_product_id}' is still NOT matched! Details: {mismatched_details}")

    print(f"{'=' * 70}\n")