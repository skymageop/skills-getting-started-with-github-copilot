import pytest


def test_get_activities(client):
    """Test retrieving all activities"""
    # Arrange
    # (No setup needed - activities are predefined in app)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert isinstance(activities, dict)
    assert len(activities) > 0
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_signup_new_participant(client):
    """Test that a new participant can sign up for an activity"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    assert email in response.json()["message"]
    
    # Verify participant was added by fetching activities
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_participant(client):
    """Test that a participant cannot sign up twice for the same activity"""
    # Arrange
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    
    # Act - First signup
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert - First signup succeeds
    assert response1.status_code == 200
    
    # Act - Second signup attempt
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert - Second signup fails
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test that signup fails for non-existent activity"""
    # Arrange
    email = "student@mergington.edu"
    activity = "Nonexistent Activity"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant(client):
    """Test that a participant can be unregistered from an activity"""
    # Arrange
    email = "test@mergington.edu"
    activity = "Programming Class"
    
    # First sign up the participant
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act - Unregister
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent_participant(client):
    """Test that unregistering a non-existent participant fails"""
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_from_nonexistent_activity(client):
    """Test that unregistering from a non-existent activity fails"""
    # Arrange
    email = "student@mergington.edu"
    activity = "Nonexistent"
    
    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
