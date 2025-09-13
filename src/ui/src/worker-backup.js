/**
 * Cloudflare Worker for MOSAIC Plane Info SPA
 * Handles static asset serving and client-side routing for Vue.js application
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Handle CORS for API requests in production
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 200,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
      });
    }

    // Proxy API requests to Django backend (configure API_BASE_URL in production)
    if (url.pathname.startsWith('/api/')) {
      const apiUrl = `${env.API_BASE_URL || 'https://your-api-domain.com'}${url.pathname}${url.search}`;
      
      const response = await fetch(apiUrl, {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });

      // Add CORS headers to API responses
      const modifiedResponse = new Response(response.body, response);
      modifiedResponse.headers.set("Access-Control-Allow-Origin", "*");
      modifiedResponse.headers.set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
      modifiedResponse.headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
      
      return modifiedResponse;
    }

    // Handle static assets and SPA routing
    const asset = await env.ASSETS.fetch(request);
    
    // If the asset exists, return it
    if (asset.status !== 404) {
      // Add security headers to HTML responses
      if (url.pathname.endsWith('.html') || url.pathname === '/') {
        const response = new Response(asset.body, asset);
        response.headers.set("X-Frame-Options", "DENY");
        response.headers.set("X-Content-Type-Options", "nosniff");
        response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
        response.headers.set("Content-Security-Policy", "default-src 'self' 'unsafe-inline' 'unsafe-eval' https:; img-src 'self' data: https:; font-src 'self' https:;");
        return response;
      }
      return asset;
    }

    // For SPA routing: serve index.html for all unmatched routes
    // This allows Vue Router to handle client-side routing
    try {
      const indexRequest = new Request(new URL('/', request.url).toString(), request);
      const indexAsset = await env.ASSETS.fetch(indexRequest);
      
      if (indexAsset.status === 200) {
        const response = new Response(indexAsset.body, {
          status: 200,
          headers: {
            "Content-Type": "text/html;charset=UTF-8",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self' 'unsafe-inline' 'unsafe-eval' https:; img-src 'self' data: https:; font-src 'self' https:;",
          },
        });
        return response;
      }
    } catch (error) {
      console.error('Error serving SPA fallback:', error);
    }

    // Fallback 404 response
    return new Response('Not Found', { 
      status: 404,
      headers: {
        "Content-Type": "text/plain"
      }
    });
  },
};