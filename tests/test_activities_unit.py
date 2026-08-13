import pytest
from src.app import activities


class TestActivitiesDataStructure:
    """Unit tests for activities data structure."""

    def test_activities_is_dictionary(self):
        """Test that activities is a dictionary."""
        assert isinstance(activities, dict)

    def test_activities_not_empty(self):
        """Test that activities dictionary is not empty."""
        assert len(activities) > 0

    def test_all_activities_have_required_fields(self):
        """Test that all activities have required fields."""
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_details in activities.items():
            assert isinstance(activity_name, str), f"Activity name should be string, got {type(activity_name)}"
            
            for field in required_fields:
                assert field in activity_details, f"Activity '{activity_name}' missing field '{field}'"
                
            # Validate field types
            assert isinstance(activity_details["description"], str)
            assert isinstance(activity_details["schedule"], str)
            assert isinstance(activity_details["max_participants"], int)
            assert isinstance(activity_details["participants"], list)

    def test_max_participants_is_positive(self):
        """Test that max_participants is a positive integer."""
        for activity_name, activity_details in activities.items():
            assert activity_details["max_participants"] > 0, \
                f"Activity '{activity_name}' has invalid max_participants"

    def test_participants_list_contains_strings(self):
        """Test that all participants are strings (emails)."""
        for activity_name, activity_details in activities.items():
            for participant in activity_details["participants"]:
                assert isinstance(participant, str), \
                    f"Participant in '{activity_name}' is not a string"

    def test_no_participant_exceeds_max_participants(self):
        """Test that no activity has more participants than max allowed."""
        for activity_name, activity_details in activities.items():
            current_count = len(activity_details["participants"])
            max_allowed = activity_details["max_participants"]
            assert current_count <= max_allowed, \
                f"Activity '{activity_name}' has {current_count} participants but max is {max_allowed}"


class TestActivitiesInitialization:
    """Unit tests for activities initialization."""

    def test_chess_club_exists(self):
        """Test that Chess Club activity exists."""
        assert "Chess Club" in activities

    def test_programming_class_exists(self):
        """Test that Programming Class activity exists."""
        assert "Programming Class" in activities

    def test_gym_class_exists(self):
        """Test that Gym Class activity exists."""
        assert "Gym Class" in activities

    def test_basketball_team_exists(self):
        """Test that Basketball Team activity exists."""
        assert "Basketball Team" in activities

    def test_tennis_club_exists(self):
        """Test that Tennis Club activity exists."""
        assert "Tennis Club" in activities

    def test_drama_club_exists(self):
        """Test that Drama Club activity exists."""
        assert "Drama Club" in activities

    def test_art_studio_exists(self):
        """Test that Art Studio activity exists."""
        assert "Art Studio" in activities

    def test_debate_team_exists(self):
        """Test that Debate Team activity exists."""
        assert "Debate Team" in activities

    def test_science_club_exists(self):
        """Test that Science Club activity exists."""
        assert "Science Club" in activities

    def test_exactly_nine_activities(self):
        """Test that exactly 9 activities exist."""
        assert len(activities) == 9

    def test_all_activities_have_descriptions(self):
        """Test that all activities have non-empty descriptions."""
        for activity_name, activity_details in activities.items():
            assert activity_details["description"], \
                f"Activity '{activity_name}' has empty description"

    def test_all_activities_have_schedules(self):
        """Test that all activities have non-empty schedules."""
        for activity_name, activity_details in activities.items():
            assert activity_details["schedule"], \
                f"Activity '{activity_name}' has empty schedule"


class TestParticipantValidation:
    """Unit tests for participant-related logic."""

    def test_participants_list_is_mutable(self):
        """Test that participants list can be modified."""
        activity = activities["Chess Club"]
        original_count = len(activity["participants"])
        
        # Try to add a participant
        test_email = "test_mutation@school.com"
        activity["participants"].append(test_email)
        
        assert len(activity["participants"]) == original_count + 1
        assert test_email in activity["participants"]
        
        # Clean up
        activity["participants"].remove(test_email)

    def test_no_duplicate_participants_initially(self):
        """Test that no activity has duplicate participants in initial state."""
        for activity_name, activity_details in activities.items():
            participants = activity_details["participants"]
            unique_participants = set(participants)
            assert len(participants) == len(unique_participants), \
                f"Activity '{activity_name}' has duplicate participants"

    def test_participant_email_format_validation(self):
        """Test that initial participants have valid email-like format."""
        for activity_name, activity_details in activities.items():
            for participant in activity_details["participants"]:
                # Basic email format check: should contain @
                assert "@" in participant, \
                    f"Participant '{participant}' in '{activity_name}' doesn't look like an email"
                assert "." in participant, \
                    f"Participant '{participant}' in '{activity_name}' doesn't look like an email"
