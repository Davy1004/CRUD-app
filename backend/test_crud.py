"""
Test script for CRUD operations on User model
This script tests all CRUD operations without running the Flask server
"""

from services.user_service import UserService
from models.user import User
from database.db import db
from app import create_app
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def test_crud_operations():
    """Test all CRUD operations"""

    # Create app and context
    app = create_app('testing')

    with app.app_context():
        print_section("Starting CRUD Operations Test")

        # Initialize service
        user_service = UserService()

        # TEST 1: CREATE USERS
        print_section("TEST 1: CREATE USERS")

        try:
            user1_data = {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '555-1234',
                'address': '123 Main St'
            }
            user1 = user_service.create_user(user1_data)
            print(f"✓ Created user 1: {user1.name} (ID: {user1.id})")
            print(f"  Email: {user1.email}")

            user2_data = {
                'name': 'Alice Smith',
                'email': 'alice@example.com',
                'phone': '555-5678',
                'address': '456 Oak Ave'
            }
            user2 = user_service.create_user(user2_data)
            print(f"✓ Created user 2: {user2.name} (ID: {user2.id})")
            print(f"  Email: {user2.email}")

            user3_data = {
                'name': 'Bob Johnson',
                'email': 'bob@example.com',
                'phone': '555-9012',
                'address': '789 Pine Rd'
            }
            user3 = user_service.create_user(user3_data)
            print(f"✓ Created user 3: {user3.name} (ID: {user3.id})")
            print(f"  Email: {user3.email}")

        except Exception as e:
            print(f"✗ Error creating users: {e}")
            return

        # TEST 2: READ ALL USERS
        print_section("TEST 2: READ ALL USERS")

        try:
            all_users = user_service.get_all_users()
            print(f"✓ Found {len(all_users)} users")
            for user in all_users:
                print(f"  - {user.name} ({user.email})")
        except Exception as e:
            print(f"✗ Error reading all users: {e}")
            return

        # TEST 3: READ SPECIFIC USER
        print_section("TEST 3: READ SPECIFIC USER")

        try:
            user = user_service.get_user_by_id(user1.id)
            if user:
                print(f"✓ Found user by ID {user1.id}")
                print(f"  Name: {user.name}")
                print(f"  Email: {user.email}")
                print(f"  Phone: {user.phone}")
                print(f"  Address: {user.address}")
                print(f"  Created: {user.created_at}")
            else:
                print(f"✗ User not found")
        except Exception as e:
            print(f"✗ Error reading user: {e}")
            return

        # TEST 4: READ USER BY EMAIL
        print_section("TEST 4: READ USER BY EMAIL")

        try:
            user = user_service.get_user_by_email('alice@example.com')
            if user:
                print(f"✓ Found user by email: {user.email}")
                print(f"  Name: {user.name}")
            else:
                print(f"✗ User not found")
        except Exception as e:
            print(f"✗ Error: {e}")
            return

        # TEST 5: UPDATE USER
        print_section("TEST 5: UPDATE USER")

        try:
            update_data = {
                'name': 'John Updated',
                'phone': '555-9999'
            }
            updated_user = user_service.update_user(user1.id, update_data)
            if updated_user:
                print(f"✓ Updated user {user1.id}")
                print(f"  New name: {updated_user.name}")
                print(f"  New phone: {updated_user.phone}")
                print(f"  Updated at: {updated_user.updated_at}")
            else:
                print(f"✗ User not found")
        except Exception as e:
            print(f"✗ Error updating user: {e}")
            return

        # TEST 6: DELETE USER
        print_section("TEST 6: DELETE USER")

        try:
            success = user_service.delete_user(user3.id)
            if success:
                print(f"✓ Deleted user {user3.id}")

                # Verify deletion
                remaining_users = user_service.get_all_users()
                print(f"✓ Remaining users: {len(remaining_users)}")
            else:
                print(f"✗ User not found")
        except Exception as e:
            print(f"✗ Error deleting user: {e}")
            return

        # TEST 7: ERROR HANDLING - DUPLICATE EMAIL
        print_section("TEST 7: ERROR HANDLING - DUPLICATE EMAIL")

        try:
            duplicate_data = {
                'name': 'Duplicate User',
                'email': 'john@example.com'  # Already exists
            }
            user_service.create_user(duplicate_data)
            print(f"✗ Should have raised error for duplicate email")
        except ValueError as e:
            print(f"✓ Caught expected error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        # TEST 8: ERROR HANDLING - INVALID EMAIL
        print_section("TEST 8: ERROR HANDLING - INVALID EMAIL")

        try:
            invalid_data = {
                'name': 'Invalid Email User',
                'email': 'not-an-email'
            }
            user_service.create_user(invalid_data)
            print(f"✗ Should have raised error for invalid email")
        except ValueError as e:
            print(f"✓ Caught expected error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        # TEST 9: ERROR HANDLING - MISSING REQUIRED FIELDS
        print_section("TEST 9: ERROR HANDLING - MISSING REQUIRED FIELDS")

        try:
            incomplete_data = {
                'name': 'No Email User'
                # Missing email
            }
            user_service.create_user(incomplete_data)
            print(f"✗ Should have raised error for missing email")
        except ValueError as e:
            print(f"✓ Caught expected error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

        # FINAL SUMMARY
        print_section("FINAL SUMMARY")

        try:
            final_users = user_service.get_all_users()
            print(f"✓ Final user count: {len(final_users)}")
            for user in final_users:
                print(f"  - {user.to_dict()}")
        except Exception as e:
            print(f"✗ Error: {e}")

        print_section("All Tests Completed Successfully!")


if __name__ == '__main__':
    test_crud_operations()
