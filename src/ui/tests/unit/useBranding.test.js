import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useBranding } from '@/composables/useBranding'

describe('useBranding', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should detect MosaicPlane.info hostname', () => {
    // Mock window.location.hostname
    Object.defineProperty(window, 'location', {
      value: { hostname: 'mosaicplane.info' },
      writable: true
    })

    const { hostname, isMosaicPlane, isAircraftDB, siteName, siteTagline } = useBranding()
    
    expect(hostname.value).toBe('mosaicplane.info')
    expect(isMosaicPlane.value).toBe(true)
    expect(isAircraftDB.value).toBe(false)
    expect(siteName.value).toBe('MosaicPlane.info')
    expect(siteTagline.value).toBe('Compare MOSAIC-Compliant Aircraft')
  })

  it('should detect AircraftDB.info hostname', () => {
    Object.defineProperty(window, 'location', {
      value: { hostname: 'aircraftdb.info' },
      writable: true
    })

    const { hostname, isMosaicPlane, isAircraftDB, siteName, siteTagline } = useBranding()
    
    expect(hostname.value).toBe('aircraftdb.info')
    expect(isMosaicPlane.value).toBe(false)
    expect(isAircraftDB.value).toBe(true)
    expect(siteName.value).toBe('AircraftDB.info')
    expect(siteTagline.value).toBe('Comprehensive Aircraft Database')
  })

  it('should default to MosaicPlane for localhost', () => {
    Object.defineProperty(window, 'location', {
      value: { hostname: 'localhost' },
      writable: true
    })

    const { hostname, isMosaicPlane, isAircraftDB, siteName } = useBranding()
    
    expect(hostname.value).toBe('localhost')
    expect(isMosaicPlane.value).toBe(true)
    expect(isAircraftDB.value).toBe(false)
    expect(siteName.value).toBe('MosaicPlane.info')
  })

  it('should set showAllAircraft based on site type', () => {
    // Test AircraftDB shows all aircraft
    Object.defineProperty(window, 'location', {
      value: { hostname: 'aircraftdb.info' },
      writable: true
    })

    const branding1 = useBranding()
    expect(branding1.showAllAircraft.value).toBe(true)

    // Test MosaicPlane shows only MOSAIC-eligible by default
    Object.defineProperty(window, 'location', {
      value: { hostname: 'mosaicplane.info' },
      writable: true
    })

    const branding2 = useBranding()
    expect(branding2.showAllAircraft.value).toBe(false)
  })

  it('should handle SSR environment gracefully', () => {
    // Simulate SSR environment where window is undefined
    const originalWindow = global.window
    delete global.window

    const { hostname, siteName } = useBranding()
    
    expect(hostname.value).toBe('localhost')
    expect(siteName.value).toBe('MosaicPlane.info')

    // Restore window
    global.window = originalWindow
  })
})