import { test, expect } from '@playwright/test';

test.describe('API Authentication Tests', () => {
  const apiBaseUrl = 'http://localhost:8000/v1';

  test('should allow GET requests without authentication', async ({ request }) => {
    // Test aircraft list endpoint
    const aircraftResponse = await request.get(`${apiBaseUrl}/aircraft/`);
    expect(aircraftResponse.ok()).toBeTruthy();
    expect(aircraftResponse.status()).toBe(200);

    // Test manufacturers list endpoint
    const manufacturersResponse = await request.get(`${apiBaseUrl}/manufacturers/`);
    expect(manufacturersResponse.ok()).toBeTruthy();
    expect(manufacturersResponse.status()).toBe(200);

    // Test individual aircraft endpoint
    const individualResponse = await request.get(`${apiBaseUrl}/aircraft/1/`);
    const individualStatus = individualResponse.status();
    expect(individualStatus === 200 || individualStatus === 404).toBeTruthy(); // 404 is OK if aircraft doesn't exist
  });

  test('should reject POST requests without authentication', async ({ request }) => {
    const newAircraft = {
      manufacturer: 1,
      model: 'Test Aircraft',
      clean_stall_speed: 45.0,
      top_speed: 120.0,
      maneuvering_speed: 100.0,
      cruise_speed: 110.0,
      seating_capacity: 2,
      retractable_gear: false,
      variable_pitch_prop: false
    };

    const response = await request.post(`${apiBaseUrl}/aircraft/`, {
      data: newAircraft
    });

    // Should be rejected with 401 Unauthorized or 403 Forbidden
    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();
  });

  test('should reject PUT requests without authentication', async ({ request }) => {
    const updatedAircraft = {
      manufacturer: 1,
      model: 'Updated Test Aircraft',
      clean_stall_speed: 50.0,
      top_speed: 125.0,
      maneuvering_speed: 105.0,
      cruise_speed: 115.0,
      seating_capacity: 2,
      retractable_gear: false,
      variable_pitch_prop: false
    };

    const response = await request.put(`${apiBaseUrl}/aircraft/1/`, {
      data: updatedAircraft
    });

    // Should be rejected with 401 Unauthorized or 403 Forbidden
    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();
  });

  test('should reject PATCH requests without authentication', async ({ request }) => {
    const partialUpdate = {
      clean_stall_speed: 42.0
    };

    const response = await request.patch(`${apiBaseUrl}/aircraft/1/`, {
      data: partialUpdate
    });

    // Should be rejected with 401 Unauthorized or 403 Forbidden
    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();
  });

  test('should reject DELETE requests without authentication', async ({ request }) => {
    const response = await request.delete(`${apiBaseUrl}/aircraft/999/`);

    // Should be rejected with 401 Unauthorized or 403 Forbidden
    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();
  });

  test('should reject manufacturer POST requests without authentication', async ({ request }) => {
    const newManufacturer = {
      name: 'Test Manufacturer',
      is_currently_manufacturing: true
    };

    const response = await request.post(`${apiBaseUrl}/manufacturers/`, {
      data: newManufacturer
    });

    // Should be rejected with 401 Unauthorized or 403 Forbidden
    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();
  });

  test('should reject manufacturer PATCH requests without authentication', async ({ request }) => {
    const partialUpdate = {
      name: 'Updated Manufacturer Name'
    };

    const response = await request.patch(`${apiBaseUrl}/manufacturers/1/`, {
      data: partialUpdate
    });

    // Should be rejected with 401 Unauthorized or 403 Forbidden
    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();
  });

  test('should reject manufacturer DELETE requests without authentication', async ({ request }) => {
    const response = await request.delete(`${apiBaseUrl}/manufacturers/999/`);

    // Should be rejected with 401 Unauthorized or 403 Forbidden
    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();
  });

  test('should provide helpful error messages for unauthenticated requests', async ({ request }) => {
    const response = await request.post(`${apiBaseUrl}/aircraft/`, {
      data: { model: 'Test' }
    });

    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();

    // Check that the response includes authentication-related error information
    const responseText = await response.text();
    expect(responseText.toLowerCase()).toMatch(/(authentication|credentials|unauthorized|forbidden)/);
  });

  test('should handle malformed authentication headers gracefully', async ({ request }) => {
    const response = await request.post(`${apiBaseUrl}/aircraft/`, {
      headers: {
        'Authorization': 'InvalidToken'
      },
      data: { model: 'Test' }
    });

    // Should still be rejected even with malformed auth header
    const status = response.status();
    expect(status === 401 || status === 403).toBeTruthy();
  });

  test('should allow OPTIONS requests for CORS preflight', async ({ request }) => {
    const response = await request.fetch(`${apiBaseUrl}/aircraft/`, {
      method: 'OPTIONS'
    });

    // OPTIONS should be allowed for CORS preflight
    const status = response.status();
    expect(status === 200 || status === 204).toBeTruthy();
  });

  test('should maintain read-only access to compare endpoint', async ({ request }) => {
    // Compare endpoint should work without authentication
    const response = await request.get(`${apiBaseUrl}/aircraft/compare/?ids=1,2`);

    // Should work or return appropriate error for invalid IDs, but not auth error
    const status = response.status();
    expect(status !== 401 && status !== 403).toBeTruthy();
  });

  test('should maintain read-only access to manufacturer aircraft endpoint', async ({ request }) => {
    // Manufacturer aircraft endpoint should work without authentication
    const response = await request.get(`${apiBaseUrl}/manufacturers/1/aircraft/`);

    // Should work or return 404 if manufacturer doesn't exist, but not auth error
    const status = response.status();
    expect(status !== 401 && status !== 403).toBeTruthy();
  });
});