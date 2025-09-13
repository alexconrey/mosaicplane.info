<template>
  <div class="mosaic">
    <div class="page-header">
      <h1>About MOSAIC Regulations</h1>
      <p class="subtitle">
        Understanding the FAA's Modernization of Special Airworthiness Certificates (MOSAIC) Final Rule
      </p>
    </div>

    <div class="content-grid">
      <!-- Overview Section -->
      <div class="card">
        <h2>What is MOSAIC?</h2>
        <p>
          The Modernization of Special Airworthiness Certificates (MOSAIC) is an FAA final rule 
          published in July 2025 that significantly expands the definition and capabilities of 
          Light Sport Aircraft (LSA) and the privileges of sport pilots.
        </p>
        <p>
          This rule represents one of the most significant changes to general aviation regulations 
          in decades, potentially making approximately 70% of the current general aviation fleet 
          accessible to sport pilots.
        </p>
        <div class="official-document">
          <p>
            📄 <strong>For complete details:</strong> View the official 
            <a 
              href="https://www.faa.gov/newsroom/MOSAIC_Final_Rule_Issuance.pdf" 
              target="_blank" 
              rel="noopener noreferrer"
              class="text-accent document-link"
            >
              FAA MOSAIC Final Rule Issuance (PDF)
            </a>
          </p>
        </div>
      </div>

      <!-- Key Dates -->
      <div class="card">
        <h2>Important Dates</h2>
        <div class="dates-grid">
          <div class="date-item">
            <div class="date-label">Final Rule Published</div>
            <div class="date-value">July 2025</div>
          </div>
          <div class="date-item">
            <div class="date-label">Sport Pilot Privileges Effective</div>
            <div class="date-value">October 22, 2025</div>
          </div>
          <div class="date-item">
            <div class="date-label">New Aircraft Certification</div>
            <div class="date-value">July 24, 2026</div>
          </div>
        </div>
      </div>

      <!-- LSA Criteria -->
      <div class="card">
        <h2>Light Sport Aircraft (LSA) Criteria Under MOSAIC</h2>
        <div class="criteria-list">
          <div class="criteria-item">
            <h4>Stall Speed</h4>
            <p>Maximum clean stall speed (Vs1) of 61 knots calibrated airspeed</p>
          </div>
          <div class="criteria-item">
            <h4>Seating Capacity</h4>
            <p>Up to 4 seats (increased from previous 2-seat limit)</p>
          </div>
          <div class="criteria-item">
            <h4>Maximum Takeoff Weight</h4>
            <p>No weight restriction (previous 1,320 lb limit removed)</p>
          </div>
          <div class="criteria-item">
            <h4>Certification Date</h4>
            <p>
              Existing aircraft certified before July 24, 2026 are eligible if they meet 
              performance requirements. New aircraft must be certified after July 24, 2026 
              to qualify as MOSAIC LSA.
            </p>
          </div>
        </div>
      </div>

      <!-- Sport Pilot Privileges -->
      <div class="card">
        <h2>Sport Pilot Privileges</h2>
        <div class="privileges-section">
          <h4>Aircraft Eligibility</h4>
          <ul>
            <li>Aircraft with clean stall speed ≤59 knots calibrated airspeed</li>
            <li>Both existing aircraft and new MOSAIC LSA (when available)</li>
          </ul>

          <h4>Passenger Limitations</h4>
          <ul>
            <li><strong>Maximum 1 passenger</strong> regardless of aircraft seating capacity</li>
            <li>If flying a 4-seat aircraft, 2 seats must remain empty</li>
          </ul>

          <h4>New Endorsement Opportunities</h4>
          <ul>
            <li>Retractable landing gear (with appropriate logbook endorsement)</li>
            <li>Variable pitch propeller (with appropriate logbook endorsement)</li>
          </ul>
        </div>
      </div>

      <!-- Private Pilot Requirements -->
      <div class="card">
        <h2>Private Pilot Requirements</h2>
        <p>
          Aircraft with clean stall speeds between 59-61 knots are eligible as MOSAIC LSA 
          but require a private pilot certificate or higher to operate. These aircraft cannot 
          be flown by sport pilots.
        </p>
      </div>

      <!-- Notable Aircraft -->
      <div class="card">
        <h2>Notable Aircraft Now Available to Sport Pilots</h2>
        <div class="aircraft-grid">
          <div class="aircraft-item">
            <h4>Cessna 172 (early models)</h4>
            <p>4 seats, 47kt stall speed</p>
          </div>
          <div class="aircraft-item">
            <h4>Cessna 150/152</h4>
            <p>2 seats, 48kt stall speed</p>
          </div>
          <div class="aircraft-item">
            <h4>Piper Cherokee 140</h4>
            <p>4 seats, 55kt stall speed</p>
          </div>
          <div class="aircraft-item">
            <h4>Piper J-3 Cub</h4>
            <p>2 seats, 38kt stall speed</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Legal Disclaimer -->
    <LegalDisclaimer />

    <!-- Back to Database -->
    <div class="navigation-section">
      <router-link to="/" class="btn btn-primary btn-large">
        ← Back to Aircraft Database
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted, nextTick } from 'vue'
import LegalDisclaimer from '../components/LegalDisclaimer.vue'

// Handle anchor scrolling when component mounts
onMounted(async () => {
  await nextTick()
  
  // Check if there's a hash in the URL
  const hash = window.location.hash
  if (hash) {
    const element = document.getElementById(hash.substring(1))
    if (element) {
      element.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start' 
      })
    }
  }
})
</script>

<style scoped>
.mosaic {
  max-width: 800px;
  margin: 0 auto;
  padding-bottom: 3rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h1 {
  color: var(--text-accent);
  margin-bottom: 1rem;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
  line-height: 1.5;
  margin: 0;
}

.content-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 3rem;
}

.dates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.date-item {
  text-align: center;
  padding: 1rem;
  background-color: var(--bg-secondary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
}

.date-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.date-value {
  font-weight: 600;
  font-size: 1.125rem;
  color: var(--text-accent);
}

.criteria-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.criteria-item h4 {
  color: var(--text-accent);
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.criteria-item p {
  margin: 0;
  color: var(--text-secondary);
}

.privileges-section h4 {
  color: var(--text-primary);
  margin: 1.5rem 0 0.5rem 0;
  font-size: 1rem;
}

.privileges-section h4:first-child {
  margin-top: 0;
}

.privileges-section ul {
  margin: 0 0 1rem 0;
  padding-left: 1.5rem;
}

.privileges-section li {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.aircraft-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.aircraft-item {
  padding: 1rem;
  background-color: var(--bg-secondary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
}

.aircraft-item h4 {
  color: var(--text-accent);
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
}

.aircraft-item p {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.official-document {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
  border-left: 4px solid var(--text-accent);
}

.official-document p {
  margin: 0;
  font-size: 0.875rem;
}

.document-link {
  font-weight: 500;
}

.navigation-section {
  text-align: center;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 600;
}

.text-accent {
  color: var(--text-accent);
  text-decoration: none;
}

.text-accent:hover {
  text-decoration: underline;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .mosaic {
    padding: 0 0.5rem 2rem 0.5rem;
  }

  .page-header {
    margin-bottom: 2rem;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .content-grid {
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .dates-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .aircraft-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .criteria-list {
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .card {
    padding: 1rem;
  }

  .date-item {
    padding: 0.75rem;
  }

  .aircraft-item {
    padding: 0.75rem;
  }

  .btn-large {
    width: 100%;
    padding: 0.75rem 1rem;
  }
}
</style>