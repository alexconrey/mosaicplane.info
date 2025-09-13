import { test, expect } from '@playwright/test';

test.describe('Aircraft Database', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load aircraft database page', async ({ page }) => {
    // Check that the page title is correct
    await expect(page).toHaveTitle(/MosaicPlane\.info/);

    // Check that the main heading is present
    await expect(page.locator('h1')).toContainText('MosaicPlane.info');
    
    // Check that the tagline is present
    await expect(page.getByText('Compare MOSAIC-Compliant Aircraft')).toBeVisible();
    
    // Check that the Aircraft Database section is present
    await expect(page.getByText('Aircraft Database')).toBeVisible();
  });

  test('should display aircraft table with data', async ({ page }) => {
    // Wait for aircraft data to load
    await page.waitForSelector('table', { timeout: 10000 });
    
    // Check that the aircraft table is present
    const table = page.locator('table');
    await expect(table).toBeVisible();
    
    // Check for table headers
    await expect(page.getByText('Aircraft')).toBeVisible();
    await expect(page.getByText('Stall Speed')).toBeVisible();
    await expect(page.getByText('Eligibility')).toBeVisible();
    
    // Check that we have aircraft rows (at least one)
    const rows = page.locator('tbody tr');
    await expect(rows).toHaveCountGreaterThan(0);
  });

  test('should show aircraft count information', async ({ page }) => {
    // Wait for data to load
    await page.waitForSelector('.badge-info', { timeout: 10000 });
    
    // Check that aircraft count badge is present and shows a number
    const countBadge = page.locator('.badge-info');
    await expect(countBadge).toBeVisible();
    await expect(countBadge).toContainText(/\d+ aircraft/);
  });

  test('should display MOSAIC info banner', async ({ page }) => {
    // Check that the MOSAIC info banner is present
    await expect(page.getByText('MOSAIC Final Rule Effective')).toBeVisible();
    await expect(page.getByText('October 22, 2025')).toBeVisible();
    await expect(page.getByText('LSA Criteria')).toBeVisible();
    await expect(page.getByText('≤61 knots stall speed')).toBeVisible();
    await expect(page.getByText('Sport Pilot')).toBeVisible();
    await expect(page.getByText('≤59 knots, 1 passenger max')).toBeVisible();
  });

  test('should have working theme toggle', async ({ page }) => {
    // Find the theme toggle button
    const themeToggle = page.getByRole('button', { name: /Switch to.*mode/ });
    await expect(themeToggle).toBeVisible();
    
    // Get initial theme
    const initialTheme = await page.getAttribute('html', 'data-theme') || 
                        await page.getAttribute('#app', 'data-theme');
    
    // Click theme toggle
    await themeToggle.click();
    
    // Wait a bit for the theme to change
    await page.waitForTimeout(100);
    
    // Check that theme has changed
    const newTheme = await page.getAttribute('html', 'data-theme') || 
                    await page.getAttribute('#app', 'data-theme');
    
    expect(newTheme).not.toBe(initialTheme);
    expect(['light', 'dark']).toContain(newTheme);
  });

  test('should have working "More Info" link', async ({ page }) => {
    // Find and click the "More Info" link
    const moreInfoLink = page.getByRole('link', { name: 'More Info' });
    await expect(moreInfoLink).toBeVisible();
    
    await moreInfoLink.click();
    
    // Should navigate to MOSAIC page
    await expect(page).toHaveURL(/.*\/mosaic/);
    await expect(page.getByText('MOSAIC Final Rule')).toBeVisible();
  });

  test('should show footer with API documentation link', async ({ page }) => {
    // Scroll to footer
    await page.locator('footer').scrollIntoViewIfNeeded();
    
    // Check that footer is present
    await expect(page.locator('footer')).toBeVisible();
    
    // Check for API documentation link
    const apiLink = page.getByRole('link', { name: 'Documentation' });
    await expect(apiLink).toBeVisible();
    await expect(apiLink).toHaveAttribute('href', '/api/docs/');
    
    // Check for legal disclaimer link
    const legalLink = page.getByRole('link', { name: 'Legal Disclaimer' });
    await expect(legalLink).toBeVisible();
  });

  test('should display eligibility legend', async ({ page }) => {
    // Wait for page to load
    await page.waitForSelector('.legend-button', { timeout: 10000 });
    
    // Find and click the legend button
    const legendButton = page.getByRole('button', { name: /Legend/ });
    await expect(legendButton).toBeVisible();
    
    await legendButton.click();
    
    // Check that legend dropdown appears
    await expect(page.getByText('Click any badge to filter aircraft')).toBeVisible();
    await expect(page.getByText('Sport Pilot')).toBeVisible();
    await expect(page.getByText('Private Pilot')).toBeVisible();
    await expect(page.getByText('MOSAIC Eligible')).toBeVisible();
    await expect(page.getByText('Not MOSAIC Eligible')).toBeVisible();
    
    // Check for endorsement badges
    await expect(page.getByText('RG')).toBeVisible();
    await expect(page.getByText('VP')).toBeVisible();
  });

  test('should handle responsive design', async ({ page }) => {
    // Test desktop view
    await page.setViewportSize({ width: 1200, height: 800 });
    await expect(page.locator('.desktop-only')).toBeVisible();
    
    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(100); // Wait for responsive changes
    
    // Mobile elements should be visible
    await expect(page.locator('.mobile-only')).toBeVisible();
    
    // Desktop-only elements should be hidden
    await expect(page.locator('.desktop-only')).toBeHidden();
  });
});