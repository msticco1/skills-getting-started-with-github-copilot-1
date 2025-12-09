def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    # ensure participants key exists
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister_flow(client):
    activity = "Basketball Team"
    email = "tester@mergington.edu"

    # Ensure email not already registered
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity}"

    # Verify participant appears in activity
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Duplicate signup should fail
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400

    # Unregister
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Unregistered {email} from {activity}"

    # Verify participant removed
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]


def test_unregister_nonexistent(client):
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 404
