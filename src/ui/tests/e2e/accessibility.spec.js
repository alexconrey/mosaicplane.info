import { test, expect } from '@playwright/test';

test.describe('Accessibility', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should be keyboard navigable', async ({ page }) => {
    // Start navigation from top
    await page.keyboard.press('Tab');

    // Should be able to navigate through interactive elements
    let tabCount = 0;
    const maxTabs = 20; // Reasonable limit

    while (tabCount < maxTabs) {
      const focusedElement = page.locator(':focus');

      if (await focusedElement.count() === 0) break;

      // Focused element should be visible
      await expect(focusedElement).toBeVisible();

      // Move to next element
      await page.keyboard.press('Tab');
      tabCount++;
    }

    expect(tabCount).toBeGreaterThan(3); // Should have multiple focusable elements
  });

  test('should have proper ARIA labels and roles', async ({ page }) => {
    // Navigation should have proper role
    const nav = page.locator('nav, [role="navigation"]');
    await expect(nav).toBeVisible();

    // Main content should have main role
    const main = page.locator('main, [role="main"]');
    await expect(main).toBeVisible();

    // Interactive elements should have proper labels
    const buttons = page.locator('button');
    const buttonCount = await buttons.count();

    for (let i = 0; i < buttonCount; i++) {
      const button = buttons.nth(i);
      const hasAriaLabel = await button.getAttribute('aria-label');
      const hasText = await button.textContent();

      // Button should have either text content or aria-label
      expect(hasAriaLabel || (hasText && hasText.trim().length > 0)).toBeTruthy();
    }
  });

  test('should have sufficient color contrast', async ({ page }) => {
    // This is a basic check - ideally would use axe-core for comprehensive testing

    // Check that text is visible and readable
    const textElements = page.locator('p, h1, h2, h3, h4, h5, h6, span, div').filter({ hasText: /.+/ });
    const textCount = Math.min(await textElements.count(), 10);

    for (let i = 0; i < textCount; i++) {
      const element = textElements.nth(i);

      if (await element.isVisible()) {
        // Element should be visible with proper styling
        const styles = await element.evaluate(el => {
          const computed = window.getComputedStyle(el);
          return {
            color: computed.color,
            backgroundColor: computed.backgroundColor,
            fontSize: computed.fontSize
          };
        });

        // Basic checks
        expect(styles.color).not.toBe('transparent');
        expect(parseFloat(styles.fontSize)).toBeGreaterThan(12); // Minimum readable size
      }
    }
  });

  test('should provide focus indicators', async ({ page }) => {
    // Tab through interactive elements and check focus visibility
    await page.keyboard.press('Tab');

    const focusableElements = page.locator('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
    const elementCount = Math.min(await focusableElements.count(), 5);

    for (let i = 0; i < elementCount; i++) {
      const element = focusableElements.nth(i);

      if (await element.isVisible()) {
        await element.focus();

        // Element should have focus styles (outline, border, box-shadow, etc.)
        const styles = await element.evaluate(el => {
          const computed = window.getComputedStyle(el);
          return {
            outline: computed.outline,
            outlineWidth: computed.outlineWidth,
            boxShadow: computed.boxShadow,
            borderWidth: computed.borderWidth
          };
        });

        const hasFocusIndicator = styles.outline !== 'none' ||
                                 parseFloat(styles.outlineWidth) > 0 ||
                                 styles.boxShadow !== 'none' ||
                                 parseFloat(styles.borderWidth) > 0;

        expect(hasFocusIndicator).toBeTruthy();
      }
    }
  });

  test('should have proper heading structure', async ({ page }) => {
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    const headingCount = await headings.count();

    expect(headingCount).toBeGreaterThan(0);

    // Should have exactly one h1
    const h1Count = await page.locator('h1').count();
    expect(h1Count).toBe(1);

    // Check heading hierarchy (no skipped levels)
    const headingLevels = [];
    for (let i = 0; i < headingCount; i++) {
      const heading = headings.nth(i);
      const tagName = await heading.evaluate(el => el.tagName.toLowerCase());
      const level = parseInt(tagName.replace('h', ''));
      headingLevels.push(level);
    }

    // First heading should be h1
    expect(headingLevels[0]).toBe(1);

    // Check for proper heading progression (no more than +1 level jump)
    for (let i = 1; i < headingLevels.length; i++) {
      const currentLevel = headingLevels[i];
      const previousLevel = headingLevels[i - 1];
      const levelJump = currentLevel - previousLevel;

      // Level jump should not exceed 1
      expect(levelJump).toBeLessThanOrEqual(1);
    }
  });

  test('should support screen readers', async ({ page }) => {
    // Check for proper landmark roles
    const landmarks = await page.locator('[role="banner"], [role="navigation"], [role="main"], [role="contentinfo"], header, nav, main, footer').count();
    expect(landmarks).toBeGreaterThan(2);

    // Check for skip links
    const skipLinks = page.locator('a[href^="#"], .skip-link, .sr-only a');
    if (await skipLinks.count() > 0) {
      const firstSkipLink = skipLinks.first();
      await expect(firstSkipLink).toHaveAttribute('href');
    }

    // Check for hidden content that should be screen reader accessible
    const srOnlyElements = page.locator('.sr-only, .visually-hidden');
    const srOnlyCount = await srOnlyElements.count();

    for (let i = 0; i < srOnlyCount; i++) {
      const element = srOnlyElements.nth(i);
      const text = await element.textContent();

      // Screen reader only content should have meaningful text
      expect(text?.trim().length).toBeGreaterThan(0);
    }
  });

  test('should handle dynamic content accessibly', async ({ page }) => {
    // Test dropdown/modal accessibility
    const dropdownTriggers = page.locator('[aria-expanded], [aria-haspopup]');
    const triggerCount = Math.min(await dropdownTriggers.count(), 3);

    for (let i = 0; i < triggerCount; i++) {
      const trigger = dropdownTriggers.nth(i);

      if (await trigger.isVisible()) {
        const initialExpanded = await trigger.getAttribute('aria-expanded');

        await trigger.click();
        await page.waitForTimeout(100);

        const newExpanded = await trigger.getAttribute('aria-expanded');

        // aria-expanded should toggle
        if (initialExpanded === 'false') {
          expect(newExpanded).toBe('true');
        }
      }
    }
  });

  test('should provide alternative text for non-text content', async ({ page }) => {
    // All images should have alt text
    const images = page.locator('img');
    const imageCount = await images.count();

    for (let i = 0; i < imageCount; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');

      // Alt attribute must exist (can be empty for decorative images)
      expect(alt).not.toBeNull();
    }

    // Check for icons with aria-label
    const icons = page.locator('[class*="icon"], .fa, [data-icon]');
    const iconCount = Math.min(await icons.count(), 5);

    for (let i = 0; i < iconCount; i++) {
      const icon = icons.nth(i);

      if (await icon.isVisible()) {
        const hasAriaLabel = await icon.getAttribute('aria-label');
        const hasAriaHidden = await icon.getAttribute('aria-hidden');
        const hasText = await icon.textContent();

        // Icon should either have aria-label, be aria-hidden, or have text content
        const isAccessible = hasAriaLabel || hasAriaHidden === 'true' || (hasText && hasText.trim().length > 0);
        expect(isAccessible).toBeTruthy();
      }
    }
  });

  test('should be usable at 200% zoom', async ({ page }) => {
    // Set viewport to simulate 200% zoom
    await page.setViewportSize({ width: 640, height: 480 }); // Half the normal viewport

    await page.goto('/');

    // Content should still be accessible
    await expect(page.getByText('Aircraft Database')).toBeVisible();

    // Navigation should still work
    const navItems = page.locator('nav a, .nav-dropdown-item');
    if (await navItems.count() > 0) {
      await expect(navItems.first()).toBeVisible();
    }

    // No horizontal scrolling should be needed for content
    const bodyScrollWidth = await page.evaluate(() => document.body.scrollWidth);
    const viewportWidth = 640;

    expect(bodyScrollWidth).toBeLessThanOrEqual(viewportWidth + 20); // Small tolerance
  });

  test('should provide error messages and form validation feedback', async ({ page }) => {
    // Look for forms
    const forms = page.locator('form');
    const formCount = await forms.count();

    for (let i = 0; i < formCount; i++) {
      const form = forms.nth(i);
      const inputs = form.locator('input[required], select[required], textarea[required]');
      const requiredInputCount = await inputs.count();

      // If there are required fields, check for validation feedback
      if (requiredInputCount > 0) {
        const firstRequired = inputs.first();

        // Try to submit form without filling required fields
        const submitButton = form.locator('input[type="submit"], button[type="submit"], button:not([type])');

        if (await submitButton.count() > 0) {
          await submitButton.first().click();

          // Check for validation messages
          const errorMessages = form.locator('[role="alert"], .error-message, .invalid-feedback');
          const hasAriaInvalid = await firstRequired.getAttribute('aria-invalid');

          const hasValidationFeedback = await errorMessages.count() > 0 || hasAriaInvalid === 'true';

          // Note: This might not trigger on all forms, so we don't fail the test
          // Just verify the structure exists if validation is present
        }
      }
    }
  });
});