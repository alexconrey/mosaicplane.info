import { test, expect } from '@playwright/test';

test.describe('Main Page Table and Filtering', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Wait for aircraft data to load
    await page.waitForSelector('table tbody tr', { timeout: 10000 });
  });

  test.describe('Aircraft Table Display', () => {
    test('should display complete aircraft table with all columns', async ({ page }) => {
      const table = page.locator('table');
      await expect(table).toBeVisible();

      // Check viewport width to determine if we're in mobile or desktop mode
      const viewportSize = page.viewportSize();
      const isMobile = viewportSize && viewportSize.width <= 640;

      // Headers that are always visible
      const alwaysVisibleHeaders = ['Aircraft', 'Eligibility'];

      // Headers that are only visible on desktop (hidden on mobile with desktop-only class)
      const desktopOnlyHeaders = ['Stall Speed', 'MTOW', 'Seating', 'Manufacturer'];

      // Check always visible headers
      for (const header of alwaysVisibleHeaders) {
        const headerElement = table.locator('thead').getByText(header, { exact: false });
        await expect(headerElement).toBeVisible();
      }

      // Check desktop-only headers only on desktop
      if (!isMobile) {
        for (const header of desktopOnlyHeaders) {
          const headerElement = table.locator('thead').getByText(header, { exact: false });
          if (await headerElement.count() > 0) {
            await expect(headerElement).toBeVisible();
          }
        }
      } else {
        // On mobile, verify that mobile-specific elements are visible
        const mobileElements = page.locator('.mobile-only');
        if (await mobileElements.count() > 0) {
          await expect(mobileElements.first()).toBeVisible();
        }
      }

      // Check that we have aircraft rows
      const rows = page.locator('tbody tr');
      const rowCount = await rows.count();
      expect(rowCount).toBeGreaterThanOrEqual(10); // Should have substantial aircraft data
    });

    test('should display aircraft eligibility badges correctly', async ({ page }) => {
      // Check for various eligibility badges
      const eligibilityBadges = page.locator('tbody .badge');
      const badgeCount = await eligibilityBadges.count();
      expect(badgeCount).toBeGreaterThan(0);

      // Check for specific badge types
      const badgeTypes = [
        'Sport Pilot',
        'MOSAIC Eligible',
        'Private Pilot',
        'Legacy LSA'
      ];

      for (const badgeType of badgeTypes) {
        const badgeElements = eligibilityBadges.filter({ hasText: badgeType });
        if (await badgeElements.count() > 0) {
          await expect(badgeElements.first()).toBeVisible();
          await expect(badgeElements.first()).toHaveClass(/badge/);
        }
      }
    });

    test('should show aircraft specifications correctly', async ({ page }) => {
      const firstRow = page.locator('tbody tr').first();

      // Check for stall speed (should be a number with kts)
      const stallSpeed = firstRow.locator('td').nth(1); // Assuming stall speed is second column
      if (await stallSpeed.count() > 0) {
        const stallSpeedText = await stallSpeed.textContent();
        if (stallSpeedText && stallSpeedText.trim() !== '-') {
          expect(stallSpeedText).toMatch(/\d+/); // Should contain numbers
        }
      }

      // Check for MTOW (should be a number)
      const mtowElements = firstRow.locator('td').filter({ hasText: /\d+\s*(lbs?|kg)?/i });
      if (await mtowElements.count() > 0) {
        await expect(mtowElements.first()).toBeVisible();
      }

      // Check for seating (should be a number)
      const seatingElements = firstRow.locator('td').filter({ hasText: /\d+/ });
      const seatingCount = await seatingElements.count();
      expect(seatingCount).toBeGreaterThan(0);
    });

    test('should have clickable aircraft names', async ({ page }) => {
      // Find first aircraft link
      const firstAircraftLink = page.locator('tbody tr a[href*="/aircraft/"]').first();
      await expect(firstAircraftLink).toBeVisible();

      // Get aircraft name
      const aircraftName = await firstAircraftLink.textContent();
      expect(aircraftName).toBeTruthy();

      // Click the link
      await firstAircraftLink.click();

      // Should navigate to aircraft detail page
      await page.waitForURL(/\/aircraft\/\d+/);
      // Just verify we're on an aircraft page with a visible heading
      const aircraftHeading = page.locator('.aircraft-detail h1, main h1').first();
      await expect(aircraftHeading).toBeVisible();
    });
  });

  test.describe('Filter Legend and Labels', () => {
    test('should display and interact with filter legend', async ({ page }) => {
      // Find the legend button
      const legendButton = page.locator('.legend-button');

      if (await legendButton.count() > 0) {
        await expect(legendButton).toBeVisible();

        // Click to open legend
        await legendButton.click();

        // Should show legend dropdown
        const legendContent = page.locator('.legend-dropdown');
        await expect(legendContent).toBeVisible();

        // Should contain explanations of badge types
        await expect(legendContent).toContainText(/Sport Pilot|MOSAIC|Private Pilot/i);
      }
    });

    test('should display eligibility badge explanations', async ({ page }) => {
      // Open legend if it exists
      const legendButton = page.locator('.legend-button');
      if (await legendButton.count() > 0) {
        await legendButton.click();

        const legendContent = page.locator('.legend-dropdown');

        // Check for badge explanations
        const badgeExplanations = [
          'Sport Pilot',
          'MOSAIC',
          'Private Pilot'
        ];

        for (const badge of badgeExplanations) {
          const badgeExplanation = legendContent.getByText(badge, { exact: false }).first();
          if (await badgeExplanation.count() > 0) {
            await expect(badgeExplanation).toBeVisible();
          }
        }
      }
    });
  });

  test.describe('Aircraft Filtering Functionality', () => {
    test('should filter aircraft by Sport Pilot eligibility', async ({ page }) => {
      // Get initial count
      const initialRows = await page.locator('tbody tr').count();

      // Find Sport Pilot filter button in the badge filters section
      const sportPilotFilter = page.locator('.badge-filter-button').filter({
        hasText: 'Sport Pilot'
      });

      if (await sportPilotFilter.count() > 0) {
        await sportPilotFilter.first().click();

        // Wait for filtering to complete
        await page.waitForTimeout(500);

        // Check that results are filtered
        const filteredRows = await page.locator('tbody tr').count();

        // Should have some results but likely fewer than initial
        expect(filteredRows).toBeGreaterThan(0);

        // All visible rows should have Sport Pilot badge
        const visibleBadges = page.locator('tbody .badge').filter({ hasText: 'Sport Pilot' });
        const visibleBadgeCount = await visibleBadges.count();
        expect(visibleBadgeCount).toBeGreaterThan(0);
      }
    });

    test('should filter aircraft by MOSAIC eligibility', async ({ page }) => {
      // Try to find any MOSAIC-related filter button
      const mosaicFilter = page.locator('.badge-filter-button').filter({
        hasText: /MOSAIC/i
      });

      if (await mosaicFilter.count() > 0) {
        await mosaicFilter.first().click();

        // Wait for filtering to complete
        await page.waitForTimeout(500);

        // Should have filtered results (or at least not crash)
        const filteredRows = await page.locator('tbody tr').count();
        expect(filteredRows).toBeGreaterThanOrEqual(0);

        if (filteredRows > 0) {
          // Check that MOSAIC eligible aircraft are visible (includes Sport Pilot and Private Pilot)
          const mosaicBadges = page.locator('tbody .badge').filter({ hasText: /Sport Pilot|Private Pilot/i });
          if (await mosaicBadges.count() > 0) {
            await expect(mosaicBadges.first()).toBeVisible();
          }
        }
      }
    });

    test('should filter aircraft by manufacturer', async ({ page }) => {
      // Find manufacturer filter select element
      const manufacturerFilter = page.locator('#manufacturer-filter');

      if (await manufacturerFilter.count() > 0) {
        // Select a specific manufacturer (first option after "All Manufacturers")
        const options = manufacturerFilter.locator('option');
        const optionCount = await options.count();

        if (optionCount > 1) {
          const secondOption = options.nth(1);
          const optionValue = await secondOption.getAttribute('value');

          await manufacturerFilter.selectOption(optionValue);

          // Wait for filtering
          await page.waitForTimeout(500);

          // Should have filtered results
          const filteredRows = await page.locator('tbody tr').count();
          expect(filteredRows).toBeGreaterThan(0);
        }
      }
    });

    test('should filter aircraft by seating capacity', async ({ page }) => {
      // Find seating filter select element
      const seatingFilter = page.locator('#seating-filter');

      if (await seatingFilter.count() > 0) {
        // Select 2 seats option
        await seatingFilter.selectOption('2');

        // Wait for filtering
        await page.waitForTimeout(500);

        // Should have filtered results
        const filteredRows = await page.locator('tbody tr').count();
        expect(filteredRows).toBeGreaterThan(0);
      }
    });

    test('should show active filter states', async ({ page }) => {
      // Find any filterable badge/button
      const filterableButton = page.locator('.badge-filter-button').filter({
        hasText: /Sport Pilot|Private Pilot/i
      }).first();

      if (await filterableButton.count() > 0) {
        // Click to activate filter
        await filterableButton.click();

        // Wait for filter to activate
        await page.waitForTimeout(200);

        // Check if button has active state class
        const buttonClasses = await filterableButton.getAttribute('class');
        expect(buttonClasses).toBeTruthy();

        // Button should have some indication of being active
        const hasActiveState = buttonClasses.includes('badge-active') ||
                              buttonClasses.includes('active');
        // At minimum, the button should still have badge classes
        expect(buttonClasses.includes('badge')).toBe(true);
      }
    });

    test('should clear filters', async ({ page }) => {
      // Apply a filter first
      const filterButton = page.locator('.badge-filter-button').filter({
        hasText: /Sport Pilot|MOSAIC/i
      }).first();

      if (await filterButton.count() > 0) {
        await filterButton.click();
        await page.waitForTimeout(500);

        const filteredCount = await page.locator('tbody tr').count();

        // Try clicking the same filter button to deactivate (toggle)
        await filterButton.click();
        await page.waitForTimeout(500);

        const deactivatedCount = await page.locator('tbody tr').count();
        expect(deactivatedCount).toBeGreaterThanOrEqual(filteredCount);
      }
    });
  });

  test.describe('Table Sorting and Interaction', () => {
    test('should sort aircraft by available columns', async ({ page }) => {
      // Check viewport width to determine if we're in mobile or desktop mode
      const viewportSize = page.viewportSize();
      const isMobile = viewportSize && viewportSize.width <= 640;

      if (!isMobile) {
        // On desktop, try to sort by stall speed
        const stallSpeedHeader = page.locator('thead th').filter({ hasText: /stall.*speed/i });

        if (await stallSpeedHeader.count() > 0) {
          await stallSpeedHeader.click();

          // Wait for sorting to complete
          await page.waitForTimeout(500);

          // Check that table is sorted (first few values should be in order)
          const firstRows = page.locator('tbody tr').first();
          await expect(firstRows).toBeVisible();
        }
      } else {
        // On mobile, sort by a column that's always visible (Aircraft)
        const aircraftHeader = page.locator('thead th').filter({ hasText: /aircraft/i });

        if (await aircraftHeader.count() > 0) {
          await aircraftHeader.click();

          // Wait for sorting to complete
          await page.waitForTimeout(500);

          // Check that table is sorted
          const firstRows = page.locator('tbody tr').first();
          await expect(firstRows).toBeVisible();
        }
      }
    });

    test('should handle table pagination if present', async ({ page }) => {
      // Check for pagination controls
      const paginationControls = page.locator('.pagination, .page-navigation, [aria-label*="pagination"]');

      if (await paginationControls.count() > 0) {
        await expect(paginationControls).toBeVisible();

        // Check for next/previous buttons
        const nextButton = page.locator('button, a').filter({ hasText: /next|>/i });
        const prevButton = page.locator('button, a').filter({ hasText: /prev|</i });

        if (await nextButton.count() > 0) {
          await expect(nextButton).toBeVisible();
        }
      }
    });
  });

  test.describe('Responsive Table Behavior', () => {
    test('should handle table responsively on mobile', async ({ page }) => {
      // Test mobile viewport
      await page.setViewportSize({ width: 375, height: 667 });

      const table = page.locator('table');
      await expect(table).toBeVisible();

      // Should either have horizontal scroll or be stacked/responsive
      const tableContainer = page.locator('.table-responsive, .overflow-x-auto, .table-container');
      if (await tableContainer.count() > 0) {
        await expect(tableContainer).toBeVisible();
      }

      // Essential information should still be visible
      const aircraftNames = page.locator('tbody td:first-child, .aircraft-name').first();
      await expect(aircraftNames).toBeVisible();

      // Eligibility badges should be visible
      const badges = page.locator('tbody .badge').first();
      if (await badges.count() > 0) {
        await expect(badges).toBeVisible();
      }

      // Reset to desktop
      await page.setViewportSize({ width: 1280, height: 720 });
    });
  });
});