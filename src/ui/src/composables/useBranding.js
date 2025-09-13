import { computed } from 'vue'

export function useBranding() {
  const hostname = computed(() => {
    if (typeof window !== 'undefined') {
      return window.location.hostname
    }
    return 'localhost'
  })

  const isAircraftDB = computed(() => {
    return hostname.value.includes('aircraftdb.info')
  })

  const isMosaicPlane = computed(() => {
    return hostname.value.includes('mosaicplane.info') || hostname.value === 'localhost'
  })

  const siteName = computed(() => {
    if (isAircraftDB.value) {
      return 'AircraftDB.info'
    }
    return 'MosaicPlane.info'
  })

  const siteTagline = computed(() => {
    if (isAircraftDB.value) {
      return 'Comprehensive Aircraft Database'
    }
    return 'Compare MOSAIC-Compliant Aircraft'
  })

  const showAllAircraft = computed(() => {
    // AircraftDB.info shows all aircraft by default
    // MosaicPlane.info shows only MOSAIC-eligible by default
    return isAircraftDB.value
  })

  return {
    hostname,
    isAircraftDB,
    isMosaicPlane,
    siteName,
    siteTagline,
    showAllAircraft
  }
}