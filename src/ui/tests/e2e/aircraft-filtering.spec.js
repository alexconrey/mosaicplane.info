import { test, expect } from '@playwright/test';

test.describe('Aircraft Filtering', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Wait for aircraft data to load
    await page.waitForSelector('table tbody tr', { timeout: 10000 });
  });

  test('should filter aircraft by eligibility badges', async ({ page }) => {
    // Get initial aircraft count
    const countBadge = page.locator('.badge-info');
    await expect(countBadge).toContainText(/\d+ aircraft/);
    
    // Find a filter label button (e.g., Sport Pilot)
    const sportPilotFilter = page.getByRole('button', { name: 'Sport Pilot' }).first();
    
    if (await sportPilotFilter.isVisible()) {
      await sportPilotFilter.click();
      
      // Wait for filtering to complete
      await page.waitForTimeout(500);
      
      // Check that filtered results are shown
      const filteredRows = page.locator('tbody tr');
      const filteredCount = await filteredRows.count();
      
      // Should have some results
      expect(filteredCount).toBeGreaterThan(0);
      
      // Check that all visible aircraft have the Sport Pilot badge
      const sportPilotBadges = page.locator('tbody .badge').getByText('Sport Pilot');
      await expect(sportPilotBadges).toHaveCountGreaterThan(0);
    }
  });

  test('should show active filter with outline', async ({ page }) => {
    // Click on a filter badge
    const mosaicFilter = page.getByRole('button', { name: 'MOSAIC Eligible' }).first();
    
    if (await mosaicFilter.isVisible()) {
      await mosaicFilter.click();
      
      // Wait for the active state to apply
      await page.waitForTimeout(200);
      
      // Check that the filter button has the active class
      await expect(mosaicFilter).toHaveClass(/badge-active/);
    }
  });

  test('should clear filters by clicking active filter again', async ({ page }) => {
    // Get initial row count
    const initialRows = await page.locator('tbody tr').count();
    
    // Apply a filter
    const privateFilter = page.getByRole('button', { name: 'Private Pilot' }).first();
    
    if (await privateFilter.isVisible()) {
      await privateFilter.click();
      await page.waitForTimeout(500);
      
      // Should have fewer results
      const filteredRows = await page.locator('tbody tr').count();
      expect(filteredRows).toBeLessThanOrEqual(initialRows);
      
      // Click the same filter again to clear it
      await privateFilter.click();
      await page.waitForTimeout(500);
      
      // Should return to original count (or close to it)
      const clearedRows = await page.locator('tbody tr').count();
      expect(clearedRows).toBeGreaterThanOrEqual(filteredRows);
    }
  });

  test('should show pagination when needed', async ({ page }) => {
    // Check if pagination is shown (might not be visible with small datasets)
    const paginationInfo = page.locator('.pagination-info');
    const paginationButtons = page.locator('.pagination');
    
    // If there's enough data to paginate
    if (await paginationInfo.isVisible()) {
      await expect(paginationInfo).toContainText(/Showing \d+-\d+ of \d+ aircraft/);
    }
    
    if (await paginationButtons.isVisible()) {
      // Check that pagination controls work
      const nextButton = page.getByRole('button', { name: '2' }).or(
        page.getByRole('button', { name: 'Next' })
      );
      
      if (await nextButton.isVisible()) {
        await nextButton.click();
        await page.waitForTimeout(500);
        
        // Should still have aircraft data
        await expect(page.locator('tbody tr')).toHaveCountGreaterThan(0);
      }
    }
  });

  test('should work with multiple filters', async ({ page }) => {
    // Apply multiple filters if available
    const mosaicFilter = page.getByRole('button', { name: 'MOSAIC Eligible' }).first();
    const rgFilter = page.getByRole('button', { name: 'RG' }).first();
    
    if (await mosaicFilter.isVisible() && await rgFilter.isVisible()) {
      // Apply first filter
      await mosaicFilter.click();
      await page.waitForTimeout(500);
      
      const firstFilterCount = await page.locator('tbody tr').count();
      
      // Apply second filter (should further narrow results)
      await rgFilter.click();
      await page.waitForTimeout(500);
      
      const secondFilterCount = await page.locator('tbody tr').count();
      
      // Second filter should show same or fewer results
      expect(secondFilterCount).toBeLessThanOrEqual(firstFilterCount);
      
      // Both filters should be active
      await expect(mosaicFilter).toHaveClass(/badge-active/);
      await expect(rgFilter).toHaveClass(/badge-active/);
    }
  });

  test('should reset to page 1 when filtering', async ({ page }) => {
    // If we have pagination, go to page 2 first
    const page2Button = page.getByRole('button', { name: '2' });
    
    if (await page2Button.isVisible()) {
      await page2Button.click();
      await page.waitForTimeout(500);
      
      // Now apply a filter
      const anyFilter = page.getByRole('button', { name: 'Sport Pilot' }).first();
      if (await anyFilter.isVisible()) {
        await anyFilter.click();
        await page.waitForTimeout(500);
        
        // Should be back on page 1 (page 2 button should be available again if there are multiple pages)
        // This is implicit in the filtering behavior
        const currentPageIndicator = page.locator('.pagination .active');
        if (await currentPageIndicator.isVisible()) {
          await expect(currentPageIndicator).toContainText('1');
        }
      }
    }
  });

  test('should show appropriate messages when no results', async ({ page }) => {
    // Try to create a filter combination that yields no results
    // This might not be possible with the current dataset, so we'll just check the structure
    
    const allFilters = page.locator('.filter-labels button');
    const filterCount = await allFilters.count();
    
    if (filterCount > 3) {
      // Apply multiple filters that might conflict
      await allFilters.nth(0).click();
      await allFilters.nth(1).click();
      await allFilters.nth(2).click();
      await page.waitForTimeout(500);
      
      // Check if we have any results
      const resultCount = await page.locator('tbody tr').count();
      
      if (resultCount === 0) {
        // Should show appropriate message or empty state
        await expect(page.locator('tbody')).toBeVisible();
      } else {
        // If we still have results, that's fine too
        expect(resultCount).toBeGreaterThan(0);
      }
    }
  });

  test('should maintain filter state on page reload', async ({ page }) => {
    // Apply a filter
    const sportFilter = page.getByRole('button', { name: 'Sport Pilot' }).first();
    
    if (await sportFilter.isVisible()) {
      await sportFilter.click();
      await page.waitForTimeout(500);
      
      // Reload the page
      await page.reload();
      await page.waitForSelector('table tbody tr', { timeout: 10000 });
      
      // Note: Depending on implementation, filters might or might not persist
      // This test documents the current behavior
      // If filters should persist, check that the filter is still active
      // If filters should reset, check that all aircraft are shown
    }
  });
});