import { test, expect } from '@playwright/test';

test.describe('Legal Disclaimer', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should have legal disclaimer link in footer', async ({ page }) => {
    // Scroll to footer to ensure it's visible
    await page.locator('footer').scrollIntoViewIfNeeded();

    // Check that the legal disclaimer link is present in footer
    const disclaimerLink = page.getByRole('link', { name: 'Legal Disclaimer' });
    await expect(disclaimerLink).toBeVisible();

    // Verify it has the correct href
    await expect(disclaimerLink).toHaveAttribute('href', '/about#legal-disclaimer');
  });

  test('should navigate to legal disclaimer when footer link is clicked', async ({ page }) => {
    // Scroll to footer and click legal disclaimer link
    await page.locator('footer').scrollIntoViewIfNeeded();
    const disclaimerLink = page.getByRole('link', { name: 'Legal Disclaimer' });

    await disclaimerLink.click();

    // Should navigate to about page with legal disclaimer anchor
    await expect(page).toHaveURL(/.*\/about#legal-disclaimer/);

    // Wait for page to load
    await page.waitForLoadState('networkidle');

    // Verify legal disclaimer section is visible
    const disclaimerSection = page.locator('#legal-disclaimer');
    await expect(disclaimerSection).toBeVisible();

    // Check for key disclaimer content
    await expect(page.getByRole('heading', { name: /Legal Disclaimer/i })).toBeVisible();
    await expect(page.getByText('Not Legal Advice')).toBeVisible();
  });

  test('should display comprehensive legal disclaimer content', async ({ page }) => {
    // Navigate directly to about page
    await page.goto('/about#legal-disclaimer');

    const disclaimerSection = page.locator('#legal-disclaimer');
    await expect(disclaimerSection).toBeVisible();

    // Check for required disclaimer elements
    await expect(disclaimerSection.getByRole('heading', { name: /Legal Disclaimer/i })).toBeVisible();

    // Verify key legal disclaimer points are present
    const disclaimerList = disclaimerSection.locator('.disclaimer-list');
    await expect(disclaimerList.getByText('Not Legal Advice')).toBeVisible();
    await expect(disclaimerList.getByText(/accuracy.*information/i)).toBeVisible();
    await expect(disclaimerList.getByText(/consult.*qualified/i)).toBeVisible();

    // Check disclaimer footer
    const disclaimerFooter = disclaimerSection.locator('.disclaimer-footer');
    await expect(disclaimerFooter).toBeVisible();
  });

  test('should be accessible with proper ARIA labels', async ({ page }) => {
    await page.goto('/about#legal-disclaimer');

    const disclaimerSection = page.locator('#legal-disclaimer');

    // Check that the section has proper accessibility structure
    const heading = disclaimerSection.getByRole('heading', { name: /Legal Disclaimer/i });
    await expect(heading).toBeVisible();

    // Verify list structure is accessible
    const list = disclaimerSection.locator('.disclaimer-list');
    await expect(list).toBeVisible();

    // Should be properly scrolled into view when navigating via anchor
    await expect(disclaimerSection).toBeInViewport();
  });

  test('should display disclaimer on MOSAIC page as well', async ({ page }) => {
    // Navigate to MOSAIC page
    await page.goto('/mosaic');

    // Scroll to bottom where disclaimer should be
    const disclaimerSection = page.locator('#legal-disclaimer');
    await disclaimerSection.scrollIntoViewIfNeeded();

    // Verify legal disclaimer is present on MOSAIC page too
    await expect(disclaimerSection).toBeVisible();
    await expect(disclaimerSection.getByRole('heading', { name: /Legal Disclaimer/i })).toBeVisible();
  });
});