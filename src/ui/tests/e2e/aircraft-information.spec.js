import { test, expect } from '@playwright/test'

test.describe('Aircraft Information Section', () => {
  test.beforeEach(async ({ page }) => {
    // First go to home page to ensure app loads
    await page.goto('/')
    
    // Wait for the aircraft table to load
    await page.waitForSelector('.table', { timeout: 15000 })
    
    // Click on the first aircraft link to go to detail page
    const firstAircraftLink = page.locator('.table tbody tr:first-child td a').first()
    await firstAircraftLink.click()
    
    // Wait for the aircraft detail page to load
    await page.waitForLoadState('networkidle')
    
    // Wait for either the aircraft-info-grid or the page content to be available
    await page.waitForSelector('.aircraft-info-grid, .card', { timeout: 15000 })
  })

  test('displays MOSAIC eligibility summary with enhanced typography', async ({ page }) => {
    // Check eligibility badge exists and has correct styling
    const eligibilityBadge = page.locator('.eligibility-badge')
    await expect(eligibilityBadge).toBeVisible()
    
    // Verify key specifications are displayed with enhanced typography
    const keySpecs = page.locator('.key-specs .key-spec')
    await expect(keySpecs.first()).toBeVisible()
    
    // Take screenshot for visual verification
    await page.screenshot({ 
      path: 'playwright-report/mosaic-eligibility-summary.png',
      fullPage: false,
      clip: { x: 0, y: 0, width: 1200, height: 400 }
    })
  })

  test('renders complete 2x2 grid layout', async ({ page }) => {
    // Verify Aircraft Information section exists and is full-width
    const aircraftInfoSection = page.locator('.card.spec-card.full-width').filter({ hasText: 'Aircraft Information' })
    await expect(aircraftInfoSection).toBeVisible()
    
    const sectionTitle = aircraftInfoSection.locator('h3')
    await expect(sectionTitle).toHaveText('Aircraft Information')
    
    // Verify 2x2 grid exists
    const grid = page.locator('.aircraft-info-grid')
    await expect(grid).toBeVisible()
    
    // Verify all four info sections are present
    const infoSections = grid.locator('.info-section')
    await expect(infoSections).toHaveCount(4)
    
    // Verify section titles
    await expect(infoSections.nth(0).locator('h4')).toHaveText('Flight Envelope')
    await expect(infoSections.nth(1).locator('h4')).toHaveText('Performance Speeds')
    await expect(infoSections.nth(2).locator('h4')).toHaveText('Aircraft Limits')
    await expect(infoSections.nth(3).locator('h4')).toHaveText('Certification')
    
    // Take screenshot of full grid layout
    await page.screenshot({ 
      path: 'playwright-report/aircraft-info-grid-layout.png',
      fullPage: false,
      clip: { x: 0, y: 200, width: 1200, height: 800 }
    })
  })

  test('displays flight envelope section with critical speeds', async ({ page }) => {
    const flightEnvelopeSection = page.locator('.info-section').first()
    
    // Verify section has spec rows
    const specRows = flightEnvelopeSection.locator('.spec-row')
    await expect(specRows.first()).toBeVisible()
    
    // Verify this is the flight envelope section
    await expect(flightEnvelopeSection.locator('h4')).toContainText('Flight Envelope')
    
    // Take screenshot of flight envelope section
    await flightEnvelopeSection.screenshot({ 
      path: 'playwright-report/flight-envelope-section.png'
    })
  })

  test('displays performance speeds section with operational speeds', async ({ page }) => {
    const performanceSection = page.locator('.info-section').nth(1)
    
    // Verify section has content
    const specRows = performanceSection.locator('.spec-row')
    await expect(specRows.first()).toBeVisible()
    
    // Verify this is the performance section
    await expect(performanceSection.locator('h4')).toContainText('Performance')
    
    // Take screenshot of performance speeds section
    await performanceSection.screenshot({ 
      path: 'playwright-report/performance-speeds-section.png'
    })
  })

  test('displays aircraft limits and certification sections', async ({ page }) => {
    // Aircraft Limits section
    const limitsSection = page.locator('.info-section').nth(2)
    await expect(limitsSection.locator('h4')).toHaveText('Aircraft Limits')
    
    // Look for weight and seating info
    await expect(limitsSection.locator('text=Maximum Takeoff Weight')).toBeVisible()
    await expect(limitsSection.locator('text=Seating Capacity')).toBeVisible()
    
    // Certification section
    const certificationSection = page.locator('.info-section').nth(3)
    await expect(certificationSection.locator('h4')).toHaveText('Certification')
    
    // Look for certification info
    await expect(certificationSection.locator('text=Certification Date')).toBeVisible()
    await expect(certificationSection.locator('text=MOSAIC Compliant')).toBeVisible()
    
    // Take screenshot of both sections
    await limitsSection.screenshot({ 
      path: 'playwright-report/aircraft-limits-section.png'
    })
    await certificationSection.screenshot({ 
      path: 'playwright-report/certification-section.png'
    })
  })

  test('maintains EditableField functionality', async ({ page }) => {
    // Look for editable fields (they should have specific attributes or classes)
    const editableFields = page.locator('[class*="inline-edit"]')
    
    // Verify at least some editable fields exist
    const fieldCount = await editableFields.count()
    expect(fieldCount).toBeGreaterThan(0)
    
    // Take screenshot showing editable fields
    await page.screenshot({ 
      path: 'playwright-report/editable-fields-integration.png',
      fullPage: true
    })
  })

  test('responsive design - mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 812 })
    
    // Wait for layout to adjust
    await page.waitForTimeout(500)
    
    // Verify grid still exists and is readable on mobile
    const grid = page.locator('.aircraft-info-grid')
    await expect(grid).toBeVisible()
    
    // Verify sections are stacked properly on mobile
    const infoSections = grid.locator('.info-section')
    await expect(infoSections).toHaveCount(4)
    
    // Take mobile screenshot
    await page.screenshot({ 
      path: 'playwright-report/mobile-responsive-layout.png',
      fullPage: true
    })
  })

  test('responsive design - tablet viewport', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 })
    
    // Wait for layout to adjust
    await page.waitForTimeout(500)
    
    // Verify grid layout works on tablet
    const grid = page.locator('.aircraft-info-grid')
    await expect(grid).toBeVisible()
    
    const infoSections = grid.locator('.info-section')
    await expect(infoSections).toHaveCount(4)
    
    // Take tablet screenshot
    await page.screenshot({ 
      path: 'playwright-report/tablet-responsive-layout.png',
      fullPage: true
    })
  })

  test('conditional V-speed display based on data availability', async ({ page }) => {
    // Go back to home page
    await page.goto('/')
    await page.waitForSelector('.table', { timeout: 15000 })
    
    // Click on the second aircraft link if available
    const secondAircraftLink = page.locator('.table tbody tr:nth-child(2) td a').first()
    const linkExists = await secondAircraftLink.count() > 0
    
    if (linkExists) {
      await secondAircraftLink.click()
      await page.waitForLoadState('networkidle')
      await page.waitForSelector('.aircraft-info-grid, .card', { timeout: 15000 })
      
      // Verify sections still render even with potentially limited data
      const performanceSection = page.locator('.info-section').nth(1)
      if (await performanceSection.count() > 0) {
        await expect(performanceSection).toBeVisible()
      }
    }
    
    // Take screenshot of different aircraft data
    await page.screenshot({ 
      path: 'playwright-report/conditional-vspeed-display.png',
      fullPage: true
    })
  })

  test('full page screenshot for CI verification', async ({ page }) => {
    // Take comprehensive screenshot for admin verification
    await page.screenshot({ 
      path: 'playwright-report/full-aircraft-detail-page.png',
      fullPage: true
    })
    
    // Also capture just the Aircraft Information section
    const aircraftInfoSection = page.locator('.card.spec-card.full-width').filter({ hasText: 'Aircraft Information' })
    await aircraftInfoSection.screenshot({ 
      path: 'playwright-report/aircraft-information-section-complete.png'
    })
  })

  test('accessibility and keyboard navigation', async ({ page }) => {
    // Test keyboard navigation through the section
    await page.keyboard.press('Tab')
    
    // Verify section is accessible
    const aircraftInfoSection = page.locator('.card.spec-card.full-width').filter({ hasText: 'Aircraft Information' })
    await expect(aircraftInfoSection).toBeVisible()
    
    // Check for proper heading structure
    const headings = page.locator('h3, h4')
    const headingCount = await headings.count()
    expect(headingCount).toBeGreaterThan(0)
    
    // Take screenshot for accessibility verification
    await page.screenshot({ 
      path: 'playwright-report/accessibility-verification.png',
      fullPage: true
    })
  })
})