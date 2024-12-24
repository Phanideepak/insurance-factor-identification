# insurance-factor-identification

Topics that are Covered:

- Creating CRUD API in fast API and SQL Alchemy
- Custom Request Validation
- JWT Authentication and Role Based Authorization
- Alembic
- Docker Integration.
- Redis Integration.
- Global exception handler on rest api
- Integrating Mongodb
- Request and Response Logginng in Mongodb

## List of CRUD API's Created

1. Auth API
   - Signup API
   - Login API
   - Forget Password API
   - Reset Password API

2. Insurance API
   - Add Insurance API (`ADMIN`)
   - Edit Insurance API (`ADMIN`)
   - Get All Insurances API (`ADMIN`, `AGENT`)
   - Get Insurance by id API (`ADMIN`, `AGENT`, `CUSTOMER`)
   - Delete Insurance by id API (`ADMIN`)

3. Customer API
   - Add Customer API (`ADMIN`)
   - Edit Customer API (`ADMIN`)
   - Get All Customers API (`ADMIN`, `AGENT`)
   - Get Customer By id API (`ADMIN`, `AGENT`, `CUSTOMER`)
   - Get Premium Enquiry API (`CUSTOMER`, `AGENT`, `ADMIN`)
   - Delete Customer by id API (`ADMIN`)

4. Agent API
   - Add Agent API (`ADMIN`)
   - Edit Agent API (`ADMIN`)
   - Get All Agents API (`ADMIN`)
   - Get Agent By Id API (`ADMIN`)
   - Delete Agent by id API (`ADMIN`)

5. Order API
   - Create Order API (`AGENT`)
   - Pay Order API (`CUSTOMER`)
   - Get Order by API (`ADMIN`, `AGENT`, `CUSTOMER`)
   - Approve Order API  (`ADMIN`)
