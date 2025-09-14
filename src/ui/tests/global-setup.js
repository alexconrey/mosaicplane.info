// Set NODE_ENV to test and use test-specific Vite config for Firefox compatibility
export default function globalSetup() {
  process.env.NODE_ENV = 'test';
  process.env.VITE_CONFIG_FILE = 'vite.config.test.js';
  process.env.PLAYWRIGHT_DIRECT_API = 'true';
}