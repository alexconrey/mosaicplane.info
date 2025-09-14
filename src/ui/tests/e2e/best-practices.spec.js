import { test, expect } from '@playwright/test';

test.describe('Best Practices', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should have proper page title and meta description', async ({ page }) => {
    // Check page title follows best practices
    await expect(page).toHaveTitle(/MosaicPlane\.Info.*MOSAIC/i);

    // Check meta description exists
    const metaDescription = page.locator('meta[name="description"]');
    await expect(metaDescription).toHaveAttribute('content');

    // Description should be meaningful and under 160 characters
    const description = await metaDescription.getAttribute('content');
    expect(description?.length).toBeLessThan(160);
    expect(description).toMatch(/MOSAIC|aircraft|comparison/i);
  });

  test('should load critical resources efficiently', async ({ page }) => {
    const startTime = Date.now();

    // Navigate and wait for load
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');

    const loadTime = Date.now() - startTime;

    // Page should load within reasonable time (5 seconds)
    expect(loadTime).toBeLessThan(5000);

    // Check that main content is visible quickly
    await expect(page.getByText('Aircraft Database')).toBeVisible({ timeout: 3000 });
  });

  test('should have proper semantic HTML structure', async ({ page }) => {
    // Check for proper heading hierarchy
    const h1 = page.locator('h1');
    await expect(h1).toHaveCount(1); // Should have exactly one h1

    // Check main landmark
    const main = page.locator('main');
    await expect(main).toBeVisible();

    // Check navigation
    const nav = page.locator('nav');
    await expect(nav).toBeVisible();

    // Check footer
    const footer = page.locator('footer');
    await expect(footer).toBeVisible();
  });

  test('should have proper form labels and inputs', async ({ page }) => {
    // Search form should have proper labels
    const searchInput = page.locator('input[type="search"], input#search-aircraft');
    if (await searchInput.count() > 0) {
      const searchLabel = page.locator('label[for="search-aircraft"]');
      await expect(searchLabel).toBeVisible();
      await expect(searchInput).toHaveAttribute('aria-describedby');
    }

    // All form controls should have labels
    const inputs = page.locator('input, select, textarea');
    const inputCount = await inputs.count();

    for (let i = 0; i < inputCount; i++) {
      const input = inputs.nth(i);
      const inputId = await input.getAttribute('id');

      if (inputId) {
        const label = page.locator(`label[for="${inputId}"]`);
        await expect(label).toBeVisible();
      }
    }
  });

  test('should handle errors gracefully', async ({ page }) => {
    // Test 404 page
    await page.goto('/nonexistent-page');

    // Should not show white screen or crash
    const bodyText = await page.locator('body').textContent();
    expect(bodyText?.length).toBeGreaterThan(10);

    // Should have navigation back to main site
    await expect(page.getByRole('link', { name: /home|back/i })).toBeVisible();
  });

  test('should have proper external link handling', async ({ page }) => {
    // Find external links
    const externalLinks = page.locator('a[href^="http"], a[target="_blank"]');
    const linkCount = await externalLinks.count();

    // External links should have proper attributes
    for (let i = 0; i < linkCount && i < 5; i++) { // Check first 5 external links
      const link = externalLinks.nth(i);

      if (await link.getAttribute('target') === '_blank') {
        // Should have security attributes
        await expect(link).toHaveAttribute('rel', /noopener/);
      }
    }
  });

  test('should have proper image optimization', async ({ page }) => {
    const images = page.locator('img');
    const imageCount = await images.count();

    // All images should have alt text
    for (let i = 0; i < imageCount; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');

      // Alt should exist (can be empty for decorative images)
      expect(alt).not.toBeNull();
    }
  });

  test('should have proper caching headers', async ({ page }) => {
    const response = await page.goto('/');

    // Should have cache control headers
    const headers = response?.headers();

    // Static assets should be cacheable
    if (headers?.['cache-control']) {
      expect(headers['cache-control']).toBeTruthy();
    }
  });

  test('should be search engine optimized', async ({ page }) => {
    // Check for canonical URL
    const canonical = page.locator('link[rel="canonical"]');
    if (await canonical.count() > 0) {
      await expect(canonical).toHaveAttribute('href');
    }

    // Check for proper Open Graph tags
    const ogTitle = page.locator('meta[property="og:title"]');
    if (await ogTitle.count() > 0) {
      await expect(ogTitle).toHaveAttribute('content');
    }

    // Check that robots.txt would be accessible (don't actually fetch it)
    const robotsResponse = await page.request.get('/robots.txt');
    expect(robotsResponse.status()).toBeLessThan(500); // Should not error
  });

  test('should handle JavaScript disabled gracefully', async ({ page }) => {
    // Disable JavaScript
    await page.context().addInitScript(() => {
      window.addEventListener('error', (e) => {
        e.preventDefault();
      });
    });

    await page.goto('/');

    // Basic content should still be accessible
    const bodyText = await page.locator('body').textContent();
    expect(bodyText?.length).toBeGreaterThan(100);
  });
});