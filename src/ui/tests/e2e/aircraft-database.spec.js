import { test, expect } from '@playwright/test';

test.describe('Aircraft Database', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load aircraft database page', async ({ page }) => {
    // Check that the page title is correct
    await expect(page).toHaveTitle(/MosaicPlane\.Info.*MOSAIC/i);

    // Check that the main heading is present
    await expect(page.locator('h1')).toContainText(/MosaicPlane\.Info/i);
    
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

    // Check for table headers within the table - Aircraft and Eligibility are always visible
    await expect(table.locator('thead').getByText('Aircraft')).toBeVisible();
    await expect(table.locator('thead').getByText('Eligibility')).toBeVisible();

    // Check viewport width to determine if we're in mobile or desktop mode
    const viewportSize = page.viewportSize();
    const isMobile = viewportSize && viewportSize.width <= 640;

    if (!isMobile) {
      // Only check for Stall Speed column on desktop (it's hidden on mobile with desktop-only class)
      await expect(table.locator('thead').getByText('Stall Speed')).toBeVisible();
    } else {
      // On mobile, stall speed info should be in mobile-only aircraft details section
      const mobileDetails = page.locator('.mobile-only .aircraft-details');
      if (await mobileDetails.count() > 0) {
        await expect(mobileDetails.first().getByText('Stall:')).toBeVisible();
      }
    }

    // Check that we have aircraft rows (at least one)
    const rows = page.locator('tbody tr');
    const rowCount = await rows.count();
    expect(rowCount).toBeGreaterThan(0);
  });

  test('should show aircraft count information', async ({ page }) => {
    // Wait for data to load
    await page.waitForSelector('.badge-info', { timeout: 10000 });
    
    // Check that aircraft count badge is present and shows a number
    const countBadge = page.locator('.badge-info').filter({ hasText: 'Total Aircraft' });
    await expect(countBadge).toBeVisible();
    await expect(countBadge).toContainText(/\d+ Total Aircraft/);
  });

  test('should display MOSAIC info banner', async ({ page }) => {
    // Check that the MOSAIC info banner is present
    const banner = page.locator('.mosaic-notice');
    await expect(banner).toBeVisible();
    await expect(banner).toContainText('October 22, 2025');
    await expect(banner).toContainText('MOSAIC becomes effective');
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
    // Find and click the "More Info" link in the info banner
    const banner = page.locator('.info-banner');
    const moreInfoLink = banner.getByRole('link', { name: 'Learn more about MOSAIC regulations' });
    await expect(moreInfoLink).toBeVisible();

    await moreInfoLink.click();

    // Wait for navigation to complete
    await page.waitForLoadState('networkidle');

    // Should navigate to MOSAIC page
    await expect(page).toHaveURL(/.*\/mosaic/);
    // Check for specific h1 heading on MOSAIC page
    await expect(page.getByRole('heading', { level: 1, name: /About MOSAIC/i })).toBeVisible({ timeout: 10000 });
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

    // Check that legend dropdown appears and wait for it to be fully visible
    const dropdown = page.locator('.legend-dropdown');
    await expect(dropdown).toBeVisible();
    await page.waitForTimeout(100); // Allow dropdown to fully render
    await expect(dropdown.getByText('Click any badge to filter aircraft')).toBeVisible();
    await expect(dropdown.locator('.badge', { hasText: 'Sport Pilot' })).toBeVisible();
    await expect(dropdown.locator('.badge', { hasText: 'Private Pilot' })).toBeVisible();
    // Check for either MOSAIC Eligible badge or just verify we have multiple badge types
    const badgeCount = await dropdown.locator('.badge').count();
    expect(badgeCount).toBeGreaterThan(3); // Should have Sport, Private, Not MOSAIC, RG, VP etc
    // Verify we have the expected badge types by checking for known ones
    const allBadges = dropdown.locator('.badge');
    const badgeTexts = await allBadges.allTextContents();

    // Should have at least Sport Pilot and Private Pilot badges
    expect(badgeTexts.some(text => text.includes('Sport Pilot'))).toBeTruthy();
    expect(badgeTexts.some(text => text.includes('Private Pilot'))).toBeTruthy();
  });

  test('should handle responsive design', async ({ page }) => {
    // Test desktop view
    await page.setViewportSize({ width: 1200, height: 800 });
    await expect(page.locator('table')).toBeVisible();

    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(100); // Wait for responsive changes

    // Table should still be visible and responsive on mobile
    await expect(page.locator('table')).toBeVisible();

    // Reset to desktop
    await page.setViewportSize({ width: 1200, height: 800 });
  });
});