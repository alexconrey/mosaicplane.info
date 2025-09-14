import { test, expect } from '@playwright/test';

test.describe('Manufacturer Pages', () => {
  test.describe('Manufacturers List Page', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/manufacturers');
      // Wait for manufacturers data to load
      await page.waitForSelector('.manufacturer-card, .manufacturer-list', { timeout: 10000 });
    });

    test('should load manufacturers page with correct title', async ({ page }) => {
      await expect(page).toHaveTitle(/MosaicPlane\.Info/i);

      // Check for main heading containing "Manufacturers"
      await expect(page.getByRole('heading', { name: /Aircraft Manufacturers/i })).toBeVisible();
    });

    test('should display manufacturer cards/list', async ({ page }) => {
      // Should have manufacturer cards or list items
      const manufacturerItems = page.locator('.manufacturer-card, .manufacturer-item, [data-testid*="manufacturer"]');
      await expect(manufacturerItems).toHaveCount(await manufacturerItems.count());
      expect(await manufacturerItems.count()).toBeGreaterThan(0);
    });

    test('should show manufacturer names and aircraft counts', async ({ page }) => {
      // Check that manufacturer names are visible
      const manufacturerNames = page.locator('.manufacturer-name, h3, h2').filter({ hasText: /\w{2,}/ });
      await expect(manufacturerNames.first()).toBeVisible();

      // Check for aircraft count information
      const countElements = page.locator(':text-matches("\\d+\\s+(aircraft|models?)", "i")');
      if (await countElements.count() > 0) {
        await expect(countElements.first()).toBeVisible();
      }
    });

    test('should have clickable manufacturer links', async ({ page }) => {
      // Find the first manufacturer link
      const firstManufacturerLink = page.locator('a[href*="/manufacturers/"]').first();
      await expect(firstManufacturerLink).toBeVisible();

      await firstManufacturerLink.click();

      // Should navigate to manufacturer detail page
      await page.waitForURL(/\/manufacturers\/\d+/);
      // Find the specific H1 with manufacturer name and verify it's visible
      const manufacturerHeading = page.locator('.manufacturer-detail h1').first();
      await expect(manufacturerHeading).toBeVisible();
      // Just check that it contains text (not empty)
      const headingText = await manufacturerHeading.textContent();
      expect(headingText.trim().length).toBeGreaterThan(0);
    });

    test('should display manufacturer logos when available', async ({ page }) => {
      // Check for manufacturer logo images
      const logoImages = page.locator('img[src*="logo"], .manufacturer-logo img, [alt*="logo" i]');
      if (await logoImages.count() > 0) {
        // At least one logo should be visible
        await expect(logoImages.first()).toBeVisible();

        // Logo should have proper alt text
        await expect(logoImages.first()).toHaveAttribute('alt', /logo|manufacturer/i);
      }
    });
  });

  test.describe('Individual Manufacturer Detail Page', () => {
    let manufacturerUrl;

    test.beforeEach(async ({ page }) => {
      // Go to manufacturers page first
      await page.goto('/manufacturers');
      await page.waitForSelector('a[href*="/manufacturers/"]', { timeout: 10000 });

      // Get the first manufacturer URL
      const firstManufacturerLink = page.locator('a[href*="/manufacturers/"]').first();
      manufacturerUrl = await firstManufacturerLink.getAttribute('href');

      // Navigate to the manufacturer detail page
      await page.goto(manufacturerUrl);
      await page.waitForSelector('h1, h2', { timeout: 10000 });
    });

    test('should load manufacturer detail page', async ({ page }) => {
      // Should have standard title
      await expect(page).toHaveTitle(/MosaicPlane\.Info/i);

      // Should have manufacturer name as heading
      const heading = page.locator('h1').first();
      await expect(heading).toBeVisible();
      await expect(heading).toContainText(/\w{2,}/);
    });

    test('should display manufacturer information', async ({ page }) => {
      // Should show manufacturer name
      const manufacturerName = page.locator('h1, h2, .manufacturer-name').first();
      await expect(manufacturerName).toBeVisible();

      // Should show manufacturing status (active/inactive)
      const statusIndicators = page.locator(':text-matches("(active|inactive|manufacturing|currently|historic)", "i")');
      if (await statusIndicators.count() > 0) {
        await expect(statusIndicators.first()).toBeVisible();
      }
    });

    test('should display manufacturer aircraft table', async ({ page }) => {
      // Should have a table of aircraft from this manufacturer
      const aircraftTable = page.locator('table, .aircraft-list, .manufacturer-aircraft');
      await expect(aircraftTable).toBeVisible();

      // Should have aircraft rows
      const aircraftRows = page.locator('tbody tr, .aircraft-item');
      const rowCount = await aircraftRows.count();
      expect(rowCount).toBeGreaterThan(0);

      // Should have aircraft names/models
      const aircraftNames = page.locator('tbody td:first-child, .aircraft-name').first();
      await expect(aircraftNames).toBeVisible();
    });

    test('should show aircraft eligibility badges', async ({ page }) => {
      // Check for MOSAIC/Sport Pilot badges in the aircraft table
      const eligibilityBadges = page.locator('.badge, .eligibility-badge').filter({
        hasText: /MOSAIC|Sport Pilot|Private Pilot|Legacy/i
      });

      if (await eligibilityBadges.count() > 0) {
        await expect(eligibilityBadges.first()).toBeVisible();
      }
    });

    test('should have clickable aircraft links', async ({ page }) => {
      // Find aircraft links in the table
      const aircraftLinks = page.locator('a[href*="/aircraft/"]');

      if (await aircraftLinks.count() > 0) {
        const firstAircraftLink = aircraftLinks.first();
        await expect(firstAircraftLink).toBeVisible();

        // Click on the first aircraft
        await firstAircraftLink.click();

        // Should navigate to aircraft detail page
        await page.waitForURL(/\/aircraft\/\d+/);
        await expect(page.locator('h1').first()).toBeVisible();
      }
    });

    test('should display V-speeds when available', async ({ page }) => {
      // Check for V-speed information in aircraft table
      const vSpeedElements = page.locator(':text-matches("V[xygf]|\\d+\\s*kts?", "i")');

      if (await vSpeedElements.count() > 0) {
        await expect(vSpeedElements.first()).toBeVisible();
      }
    });

    test('should have responsive design', async ({ page }) => {
      // Test mobile viewport
      await page.setViewportSize({ width: 375, height: 667 });

      // Should still show manufacturer name
      const heading = page.locator('h1').first();
      await expect(heading).toBeVisible();

      // Aircraft table should be responsive or have horizontal scroll
      const table = page.locator('table');
      if (await table.count() > 0) {
        await expect(table).toBeVisible();

        // Check if table is scrollable or stacked for mobile
        const tableContainer = page.locator('.table-responsive, .overflow-x-auto');
        if (await tableContainer.count() > 0) {
          await expect(tableContainer).toBeVisible();
        }
      }

      // Reset to desktop
      await page.setViewportSize({ width: 1280, height: 720 });
    });
  });

  test.describe('Manufacturer Navigation', () => {
    test('should navigate between manufacturers and main page', async ({ page }) => {
      // Start at home
      await page.goto('/');

      // Find navigation to manufacturers page
      const manufacturersNav = page.locator('a[href="/manufacturers"], a').filter({ hasText: /manufacturers/i });

      if (await manufacturersNav.count() > 0) {
        await manufacturersNav.first().click();
        await page.waitForURL(/\/manufacturers$/);

        // Should be on manufacturers page
        await expect(page.locator('h1').first()).toContainText(/manufacturers/i);

        // Navigate back to home
        const homeLink = page.locator('a[href="/"], .navbar-brand, a').filter({ hasText: /home|mosaicplane/i }).first();
        await homeLink.click();
        await page.waitForURL('/');

        // Should be back on home page
        await expect(page.locator('h1')).toContainText(/mosaicplane/i);
      }
    });
  });
});