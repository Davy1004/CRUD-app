# CRUD API - Postman Testing Guide

## Overview
This guide covers how to use Postman to test all CRUD operations for the Flask CRUD API.

## Prerequisites
- **Postman** installed ([Download here](https://www.postman.com/downloads/))
- **Flask Backend** running on `http://localhost:5000`
- **CRUD_API_Collection.postman_collection.json** imported into Postman

## Quick Start

### 1. Import Collection
1. Open Postman
2. Click **File** → **Import**
3. Select **CRUD_API_Collection.postman_collection.json**
4. Click **Import**

### 2. Set Environment Variables
The collection uses environment variables for base URL and test data:

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `http://localhost:5000` | Flask API base URL |
| `user_name` | `Test User` | Default user name for tests |
| `user_email` | `testuser@example.com` | Default user email |
| `user_phone` | `555-1234` | Default phone number |
| `user_address` | `123 Test Street` | Default address |
| `update_name` | `Updated Test User` | Updated name for PUT tests |

To set environment variables:
1. Click the **Environment** dropdown (top-right)
2. Create a new environment or use "CRUD App Testing"
3. Add the variables above
4. Select the environment before running tests

## API Endpoints Reference

### 1. Health Check
**GET** `/api/health`

Check if the API is running.

**Response (200 OK):**
```json
{
  "status": "API is running"
}
```

---

### 2. Create User
**POST** `/api/users`

Create a new user in the database.

**Request Body:**
```json
{
  "name": "Test User",
  "email": "testuser@example.com",
  "phone": "555-1234",
  "address": "123 Test Street"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "name": "Test User",
    "email": "testuser@example.com",
    "phone": "555-1234",
    "address": "123 Test Street",
    "created_at": "2026-06-16T12:22:06.274686",
    "updated_at": "2026-06-16T12:22:06.274686"
  }
}
```

**Test Script:**
- ✓ Status code is 201
- ✓ Response has success message
- ✓ User object has all fields
- ✓ User ID saved for future tests

---

### 3. Get All Users
**GET** `/api/users`

Retrieve all users from the database.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Test User",
    "email": "testuser@example.com",
    "phone": "555-1234",
    "address": "123 Test Street",
    "created_at": "2026-06-16T12:22:06.274686",
    "updated_at": "2026-06-16T12:22:06.274686"
  },
  {
    "id": 2,
    "name": "Another User",
    "email": "another@example.com",
    "phone": "555-5678",
    "address": "456 Test Ave",
    "created_at": "2026-06-16T12:23:00.000000",
    "updated_at": "2026-06-16T12:23:00.000000"
  }
]
```

**Test Script:**
- ✓ Status code is 200
- ✓ Response is an array
- ✓ Each user has required fields
- ✓ User count stored for validation

---

### 4. Get User by ID
**GET** `/api/users/{id}`

Retrieve a specific user by ID.

**URL Parameters:**
- `id` (integer) - The user ID

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Test User",
  "email": "testuser@example.com",
  "phone": "555-1234",
  "address": "123 Test Street",
  "created_at": "2026-06-16T12:22:06.274686",
  "updated_at": "2026-06-16T12:22:06.274686"
}
```

**Test Script:**
- ✓ Status code is 200
- ✓ Returned user has correct ID
- ✓ User data is complete with timestamps

---

### 5. Update User
**PUT** `/api/users/{id}`

Update an existing user's information.

**URL Parameters:**
- `id` (integer) - The user ID to update

**Request Body:**
```json
{
  "name": "Updated Test User",
  "phone": "555-9999",
  "address": "Updated Address"
}
```

**Response (200 OK):**
```json
{
  "message": "User updated successfully",
  "user": {
    "id": 1,
    "name": "Updated Test User",
    "email": "testuser@example.com",
    "phone": "555-9999",
    "address": "Updated Address",
    "created_at": "2026-06-16T12:22:06.274686",
    "updated_at": "2026-06-16T12:24:00.000000"
  }
}
```

**Test Script:**
- ✓ Status code is 200
- ✓ Response has success message
- ✓ Updated user has new values
- ✓ Updated_at timestamp is newer

---

### 6. Delete User
**DELETE** `/api/users/{id}`

Delete a user from the database.

**URL Parameters:**
- `id` (integer) - The user ID to delete

**Response (200 OK):**
```json
{
  "message": "User deleted successfully"
}
```

**Test Script:**
- ✓ Status code is 200
- ✓ Response has success message

---

## Error Scenarios

### Error: 404 Not Found
**GET** `/api/users/99999`

When requesting a non-existent user.

**Response:**
```json
{
  "error": "User not found"
}
```

---

### Error: 400 Bad Request (Missing Fields)
**POST** `/api/users`

```json
{
  "name": "Test User"
}
```

**Response:**
```json
{
  "error": "Missing required fields: name, email"
}
```

---

### Error: 400 Bad Request (Invalid Email)
**POST** `/api/users`

```json
{
  "name": "Test User",
  "email": "not-an-email"
}
```

**Response:**
```json
{
  "error": "Invalid email format"
}
```

---

## Running Tests

### Method 1: Manual Testing
1. Open the request
2. Click **Send**
3. Review response in the **Body**, **Headers**, **Tests** tabs

### Method 2: Runner
1. Click **Runner** in top-left
2. Select **CRUD App API Testing** collection
3. Select environment
4. Click **Run CRUD App API Testing**
5. View results in the **Test Results** tab

### Method 3: Automated Testing
1. Save collection
2. Use **Postman CLI**: `postman login` and `postman collection run "CRUD_API_Collection.postman_collection.json"`

## Test Execution Order

For complete testing, run requests in this order:

1. ✓ **Health Check** - Verify API is running
2. ✓ **Get All Users** - See existing users
3. ✓ **Create New User** - Add test user
4. ✓ **Get User by ID** - Retrieve created user
5. ✓ **Update User** - Modify user data
6. ✓ **Delete User** - Remove user
7. ✓ **Error: Get Non-existent User** - Test 404 handling
8. ✓ **Error: Missing Required Fields** - Test validation
9. ✓ **Error: Invalid Email Format** - Test email validation

## Performance Tips

1. **Use Collections** instead of individual requests
2. **Set environment variables** to avoid hardcoding values
3. **Use Tests tab** to validate responses automatically
4. **Monitor performance** using the response time indicator
5. **Use Postman Variables** for dynamic data

## Common Issues

| Issue | Solution |
|-------|----------|
| Connection refused | Ensure Flask backend is running on `http://localhost:5000` |
| CORS error | Backend CORS is configured for Angular (port 4200) |
| 404 errors | Check that user ID exists in database |
| Validation errors | Review request body for required fields |
| Timeout errors | Increase Postman timeout in Settings |

## Response Examples by Status Code

| Code | Meaning | Example |
|------|---------|---------|
| **200** | OK | GET request successful |
| **201** | Created | POST request successful |
| **400** | Bad Request | Invalid input or missing fields |
| **404** | Not Found | User ID doesn't exist |
| **500** | Server Error | Unexpected backend error |

## Next Steps

1. ✓ Complete CRUD API testing with Postman
2. ✓ Review test results and logs
3. ✓ Monitor backend logs for errors
4. ✓ Use Angular debugging utilities in browser console
5. ✓ Refactor code based on findings

## Additional Resources

- [Postman Documentation](https://learning.postman.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpwg.org/specs/rfc9110.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
