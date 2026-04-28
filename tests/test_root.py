def test_root_redirect(client):
    """Test that root path redirects to static HTML"""
    # Arrange
    # (No setup needed)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]
