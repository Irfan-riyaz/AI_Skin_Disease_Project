# Admin Dashboard - User Guide

## Overview
The admin dashboard provides complete system management capabilities with real-time statistics and editable user fields.

## Statistics Cards
The dashboard displays four key metrics with exact numbers fetched from the backend:
- **Total Users**: Count of all registered user accounts
- **Total Predictions**: Number of analyses performed (currently 0)
- **Total Feedback**: Count of user feedback submissions

These numbers auto-refresh every 30 seconds without requiring a page reload.

## User Management

### Viewing Users
All registered users are displayed in a table with:
- Username
- Email address
- Phone number
- Account registration date
- User type (User/Admin)
- Action buttons (Delete)

### Editing User Email
1. Click on the email address (shown in blue)
2. A dialog box will appear with the current email
3. Enter the new email address
4. Email validation will check format (must be valid email)
5. Changes save automatically to the database
6. Stats refresh automatically

**Email Validation Rules:**
- Cannot be empty
- Must contain @ symbol
- Must have domain (e.g., example.com)

### Editing User Phone
1. Click on the phone number (shown in blue)
2. A dialog box will appear with the current phone
3. Enter the new phone number
4. Press OK to save
5. Changes save automatically to the database
6. Display shows "N/A" if no phone is entered

### Changing User Type
1. Use the dropdown select next to each user
2. Options: "User" or "Admin"
3. Selection auto-saves immediately (no confirmation needed)
4. Database updates instantly
5. Stats refresh automatically

**Note:** Admin users can access the admin dashboard; regular users cannot.

### Deleting Users
1. Click the "🗑️ Delete" button next to a user
2. A confirmation dialog appears
3. Click "OK" to confirm deletion
4. User is removed from database immediately
5. Stats update automatically

## Feedback Management

### Viewing Feedback
All user feedback is displayed with:
- User name
- User email
- Feedback message
- Submission date
- Delete button

### Total Feedback Count
The exact count of feedback submissions is displayed prominently above the feedback list.

### Deleting Feedback
1. Click the "🗑️ Delete" button next to feedback
2. A confirmation dialog appears
3. Click "OK" to confirm deletion
4. Feedback is removed from database immediately
5. Feedback count updates automatically

## Real-Time Updates
- **Automatic Refresh**: Statistics refresh every 30 seconds
- **Instant Updates**: User edits update immediately
- **Live Counts**: User and feedback counts update after any change

## Filter Options
The dashboard includes filter buttons for:

**Users Tab:**
- All (shows all users)
- Active (shows active accounts)
- Users (shows regular users only)
- Admins (shows admin users only)

**Feedback Tab:**
- All (shows all feedback)
- Recent (shows newest first)
- Positive (shows positive feedback)

## Backend API Endpoints

### Get Statistics
```
GET /api/admin/stats
Response: {total_users, regular_users, admin_count, total_feedback, predictions}
```

### Update User
```
PUT /api/admin/user/{user_id}
Body: {email, phone, account_type}
```

### Delete User
```
DELETE /api/admin/user/{user_id}
```

### Delete Feedback
```
DELETE /api/admin/feedback/{feedback_id}
```

## Troubleshooting

### Stats Not Updating
- Refresh the page (Ctrl+R)
- Wait 30 seconds for auto-refresh
- Check browser console for errors (F12)

### Changes Not Saving
- Ensure you're logged in as an admin
- Check that the email format is valid (if editing email)
- Check browser console for error messages
- Try the operation again

### Internal Server Error
- Refresh the page
- Restart the Flask server
- Check that the database file exists (app.db)

## Security Notes
- Only admin users can access this dashboard
- All changes are logged in the database
- User deletion is permanent and cannot be undone
- Phone and email fields accept any input (validation for email only)

