<template>
  <div class="about">
    <div class="page-header">
      <h1>About This Website</h1>
      <p class="subtitle">
        Legal disclaimer and important information
      </p>
    </div>

    <!-- Legal Disclaimer -->
    <LegalDisclaimer />

    <!-- Additional Resources -->
    <div class="card">
      <h2>Additional Resources</h2>
      <p>
        For detailed information about MOSAIC regulations and how they affect sport pilot privileges, 
        visit our <router-link to="/mosaic" class="text-accent">MOSAIC Information page</router-link>.
      </p>
      <div class="resources-list">
        <h4>Official Sources</h4>
        <ul>
          <li>
            <a href="https://www.faa.gov/newsroom/MOSAIC_Final_Rule_Issuance.pdf" 
               target="_blank" rel="noopener" class="text-accent">
              FAA MOSAIC Final Rule Issuance (PDF)
            </a>
          </li>
          <li>
            <a href="https://www.eaa.org/" target="_blank" rel="noopener" class="text-accent">
              Experimental Aircraft Association (EAA)
            </a>
          </li>
          <li>
            <a href="https://www.faa.gov/about/office_org/headquarters_offices/avs/offices/afx/afs/afs800/afs820/" 
               target="_blank" rel="noopener" class="text-accent">
              FAA Flight Standards Service
            </a>
          </li>
        </ul>
      </div>
    </div>

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
.about {
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


.resources-list {
  margin-top: 1.5rem;
}

.resources-list h4 {
  color: var(--text-primary);
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
}

.resources-list ul {
  margin: 0;
  padding-left: 1.5rem;
}

.resources-list li {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
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
  .about {
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
}

@media (max-width: 480px) {
  .card {
    padding: 1rem;
  }

  .btn-large {
    width: 100%;
    padding: 0.75rem 1rem;
  }
}
</style>