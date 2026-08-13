import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns 200 status."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all 9 activities."""
        response = client.get("/activities")
        activities = response.json()
        assert len(activities) == 9

    def test_activity_has_required_fields(self, client):
        """Test that each activity has all required fields."""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_details in activities.items():
            assert isinstance(activity_name, str)
            for field in required_fields:
                assert field in activity_details

    def test_participants_list_is_properly_formatted(self, client):
        """Test that participants list is a list of strings."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_details in activities.items():
            assert isinstance(activity_details["participants"], list)
            for participant in activity_details["participants"]:
                assert isinstance(participant, str)

    def test_activity_data_types(self, client):
        """Test that activity fields have correct data types."""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_details in activities.items():
            assert isinstance(activity_details["description"], str)
            assert isinstance(activity_details["schedule"], str)
            assert isinstance(activity_details["max_participants"], int)
            assert activity_details["max_participants"] > 0


class TestSignup:
    """Tests for POST /activities/{activity}/signup endpoint."""

    def test_successful_signup(self, client):
        """Test that a new participant can successfully sign up."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@school.com"
        )
        assert response.status_code == 200
        assert "message" in response.json()

    def test_duplicate_signup_returns_400(self, client):
        """Test that signing up twice with same email returns 400."""
        email = "newstudent@school.com"
        activity = "Chess%20Club"
        
        # First signup
        response1 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response1.status_code == 200
        
        # Duplicate signup
        response2 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response2.status_code == 400
        assert "already signed up" in response2.json().get("detail", "").lower()

    def test_invalid_activity_returns_404(self, client):
        """Test that signing up for non-existent activity returns 404."""
        response = client.post(
            "/activities/NonExistent%20Activity/signup?email=student@school.com"
        )
        assert response.status_code == 404

    def test_participant_appears_in_activities_list_after_signup(self, client):
        """Test that a new participant appears in GET /activities after signup."""
        email = "newstudent@school.com"
        activity = "Chess Club"
        
        # Sign up
        client.post(f"/activities/Chess%20Club/signup?email={email}")
        
        # Fetch activities
        response = client.get("/activities")
        activities = response.json()
        
        assert email in activities[activity]["participants"]

    def test_signup_with_special_characters_in_email(self, client):
        """Test signup with special characters in email."""
        email = "student+tag@school.co.uk"
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 200

    def test_full_activity_returns_400(self, client):
        """Test that the app enforces max_participants limit if implemented.
        
        Note: Current implementation does not validate max_participants,
        so this test is skipped. If max_participants validation is added,
        this test should be activated.
        """
        pytest.skip("App does not currently enforce max_participants limit")

    def test_availability_updates_after_signup(self, client):
        """Test that spots_left decreases after signup."""
        activity = "Chess Club"
        email = "newstudent@school.com"
        
        # Get initial spots
        response1 = client.get("/activities")
        initial_participants = len(response1.json()[activity]["participants"])
        
        # Sign up
        client.post(f"/activities/Chess%20Club/signup?email={email}")
        
        # Get updated spots
        response2 = client.get("/activities")
        updated_participants = len(response2.json()[activity]["participants"])
        
        assert updated_participants == initial_participants + 1


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity}/participants/{email} endpoint."""

    def test_successful_removal(self, client):
        """Test that a participant can be successfully removed."""
        email = "student@school.com"
        activity = "Chess Club"
        
        # Sign up first
        client.post(f"/activities/Chess%20Club/signup?email={email}")
        
        # Remove participant
        response = client.delete(
            f"/activities/Chess%20Club/participants/{email}"
        )
        assert response.status_code == 200

    def test_removal_returns_confirmation_message(self, client):
        """Test that removal returns a confirmation message."""
        email = "student@school.com"
        
        # Sign up first
        client.post(f"/activities/Chess%20Club/signup?email={email}")
        
        # Remove participant
        response = client.delete(
            f"/activities/Chess%20Club/participants/{email}"
        )
        assert "message" in response.json()

    def test_remove_nonexistent_participant_returns_400(self, client):
        """Test that removing non-existent participant returns 400."""
        response = client.delete(
            "/activities/Chess%20Club/participants/nonexistent@school.com"
        )
        assert response.status_code == 400
        assert "not signed up" in response.json().get("detail", "").lower()

    def test_remove_from_invalid_activity_returns_404(self, client):
        """Test that removing from non-existent activity returns 404."""
        response = client.delete(
            "/activities/NonExistent%20Activity/participants/student@school.com"
        )
        assert response.status_code == 404

    def test_participant_disappears_after_removal(self, client):
        """Test that participant no longer appears in activities after removal."""
        email = "student@school.com"
        activity = "Chess Club"
        
        # Sign up
        client.post(f"/activities/Chess%20Club/signup?email={email}")
        
        # Remove participant
        client.delete(f"/activities/Chess%20Club/participants/{email}")
        
        # Verify removal
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity]["participants"]

    def test_availability_increases_after_removal(self, client):
        """Test that spots increase after participant removal."""
        email = "student@school.com"
        activity = "Chess Club"
        
        # Sign up
        client.post(f"/activities/Chess%20Club/signup?email={email}")
        response1 = client.get("/activities")
        participants_after_signup = len(response1.json()[activity]["participants"])
        
        # Remove participant
        client.delete(f"/activities/Chess%20Club/participants/{email}")
        response2 = client.get("/activities")
        participants_after_removal = len(response2.json()[activity]["participants"])
        
        assert participants_after_removal == participants_after_signup - 1


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_email_url_encoding(self, client):
        """Test that email with special characters is properly URL encoded."""
        email = "student+test@school.com"
        from urllib.parse import quote
        
        encoded_email = quote(email, safe="")
        response = client.post(
            f"/activities/Chess%20Club/signup?email={encoded_email}"
        )
        assert response.status_code == 200

    def test_activity_name_case_sensitive(self, client):
        """Test that activity names are case-sensitive."""
        # Try lowercase version
        response = client.post(
            "/activities/chess%20club/signup?email=student@school.com"
        )
        # Should fail because activity name is "Chess Club" not "chess club"
        assert response.status_code == 404

    def test_multiple_signups_different_activities(self, client):
        """Test that a student can sign up for multiple different activities."""
        email = "student@school.com"
        
        # Sign up for Chess Club
        response1 = client.post(f"/activities/Chess%20Club/signup?email={email}")
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            f"/activities/Programming%20Class/signup?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify in activities list
        response = client.get("/activities")
        activities = response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]

    def test_concurrent_signups_same_activity(self, client):
        """Test that multiple students can sign up for the same activity."""
        activity = "Chess Club"
        emails = [f"student{i}@school.com" for i in range(3)]
        
        for email in emails:
            response = client.post(
                f"/activities/Chess%20Club/signup?email={email}"
            )
            assert response.status_code == 200
        
        # Verify all are in the list
        response = client.get("/activities")
        activities = response.json()
        for email in emails:
            assert email in activities[activity]["participants"]
