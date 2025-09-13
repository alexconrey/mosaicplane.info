<template>
  <div id="legal-disclaimer" class="disclaimer-section">
    <div class="card disclaimer-card">
      <h2>⚠️ Legal Disclaimer</h2>
      <div class="disclaimer-content">
        <p><strong>Important Notice:</strong></p>
        
        <ul class="disclaimer-list">
          <li>
            <strong>Not Legal Advice:</strong> The creators of this website are not attorneys, 
            aviation lawyers, or official representatives of the Federal Aviation Administration (FAA).
          </li>
          <li>
            <strong>AI-Generated Summary:</strong> The information on this website was summarized 
            using Claude AI and should not be considered an authoritative interpretation of FAA regulations.
          </li>
          <li>
            <strong>Official Sources Required:</strong> For authoritative information regarding FAA 
            regulations, aircraft eligibility, or pilot privileges, consult:
            <ul>
              <li>The official FAA MOSAIC Final Rule documentation</li>
              <li>The Experimental Aircraft Association (EAA)</li>
              <li>A qualified aviation attorney</li>
              <li>Your local Flight Standards District Office (FSDO)</li>
            </ul>
          </li>
          <li>
            <strong>No Warranty:</strong> We make no warranties regarding the accuracy, completeness, 
            or currency of the information provided. Regulations and interpretations may change.
          </li>
          <li>
            <strong>Use at Your Own Risk:</strong> Any decisions made based on information from this 
            website are solely your responsibility. Always verify information through official channels 
            before making aviation-related decisions.
          </li>
        </ul>

        <div class="disclaimer-footer">
          <p>
            <strong>For Questions:</strong> Contact the 
            <a href="https://www.eaa.org/" target="_blank" rel="noopener" class="text-accent">
              Experimental Aircraft Association (EAA)
            </a> 
            or consult with an aviation attorney in your area.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.disclaimer-section {
  margin-bottom: 3rem;
  scroll-margin-top: 2rem; /* Accounts for fixed header or spacing */
}

.disclaimer-card {
  border-left: 4px solid var(--warning-color);
  background-color: var(--bg-secondary);
}

.disclaimer-card h2 {
  color: var(--warning-color);
  margin-bottom: 1.5rem;
}

.disclaimer-content {
  line-height: 1.6;
}

.disclaimer-content p {
  margin-bottom: 1rem;
}

.disclaimer-list {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.disclaimer-list li {
  margin-bottom: 1rem;
  color: var(--text-secondary);
}

.disclaimer-list li strong {
  color: var(--text-primary);
}

.disclaimer-list ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.disclaimer-list ul li {
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
}

.disclaimer-footer {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.disclaimer-footer p {
  margin: 0;
  font-size: 0.875rem;
  text-align: center;
}

.text-accent {
  color: var(--text-accent);
  text-decoration: none;
}

.text-accent:hover {
  text-decoration: underline;
}
</style>