import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests-ui',
  reporter: [['html', { outputFolder: 'result/ui-report', open: 'never' }], ['list']],
  use: {
    baseURL: process.env.BASE_URL || 'http://127.0.0.1:5001',
    trace: 'on-first-retry',
    video: 'on',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  outputDir: 'result/ui-artifacts',
});

