import requests
import json

def test_upload():
    url = "http://127.0.0.1:5000/upload"
    file_path = "mock_resume.docx"
    
    print(f"Sending POST upload request for '{file_path}' to {url}...")
    
    try:
        # Open file in binary mode
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
            headers = {'X-Requested-With': 'XMLHttpRequest'} # To get JSON response
            
            response = requests.post(url, files=files, headers=headers)
            
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        # Verify response structure
        data = response.json()
        assert data.get('success') is True, "Upload failed"
        assert 'candidate_id' in data, "No candidate_id returned"
        print("\nAPI Upload & Parse Test: SUCCESS!")
        
        # Fetch parsed candidate details
        candidate_id = data['candidate_id']
        details_url = f"http://127.0.0.1:5000/api/export/{candidate_id}"
        print(f"\nFetching parsed details from {details_url}...")
        details_resp = requests.get(details_url)
        print(f"Status Code: {details_resp.status_code}")
        print(json.dumps(details_resp.json(), indent=2))
        
        details = details_resp.json()
        assert details['name'] == "John Doe", f"Expected John Doe, got {details['name']}"
        assert "Flask" in details['skills'], "Expected Flask in skills"
        assert len(details['education']) > 0, "Expected education records"
        assert len(details['experience']) > 0, "Expected experience records"
        print("\nCandidate Data Verification: SUCCESS!")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_upload()
