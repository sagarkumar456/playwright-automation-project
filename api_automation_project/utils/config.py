# api_automation_project/utils/config.py

BASE_URL_TEST = "https://test.onelap.in"
BASE_URL_8443 = "https://test.onelap.in:8443/OnelapinBackendSpring-0.0.1-SNAPSHOT"

# Tokens from your curl commands
TOKEN_1 = "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI3NTI5OTQxMzc4Iiwic2NvcGVzIjpbIkFETUlOIiwiTU9ERVJBVE9SIl0sImV4cCI6MTc3ODc2Nzk3N30.d-XZ_NjvuVeHzWF8duEW6R36DyZnq5dit0qsGxZjPZfC9201wu5_LAameFU4m-fZ3kEOGjp1av7hNospoWWdsA"
TOKEN_2 = "Bearer Atza|eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI3NTI5OTQxMzc4Iiwic2NvcGVzIjpbIkFETUlOIiwiTU9ERVJBVE9SIl0sImV4cCI6MTc3ODgyODM2OH0.bWuXDHudBmLgTy5Orr6d3mo_kF3N9iCD5xITy2KNWnMg2081D3fLuM1UATvDk3aWw9EZ3y_tiPJf2amBD6q_PQ"

HEADERS_JSON_TOKEN_2 = {
    "Authorization": TOKEN_2,
    "Content-Type": "application/json"
}

HEADERS_TOKEN_1 = {
    "Authorization": TOKEN_1
}