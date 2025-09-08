import { test, expect } from '@playwright/test';

function rand(prefix: string) {
  return prefix + '-' + Math.random().toString(36).slice(2, 8);
}

test.describe('Admin User Management', () => {
  // Before each test, login as admin
  test.beforeEach(async ({ page, baseURL }) => {
    await page.goto(baseURL + '/login');
    await page.locator('#username').fill('admin');
    await page.locator('#password').fill('admin');
    await page.getByRole('button', { name: '로그인' }).click();
    await expect(page.getByText('안녕하세요, admin님')).toBeVisible();
  });

  test('should show confirmation on delete and reset password', async ({ page, baseURL }) => {
    const username = rand('testuser');
    const password = 'password';

    // Navigate to admin page
    await page.getByRole('link', { name: '사용자 관리' }).click();
    await page.waitForURL('**/admin/users');

    // Add a new user to test with
    await page.locator('#username').fill(username);
    await page.locator('#password').fill(password);
    await page.getByRole('button', { name: '추가' }).click();
    await expect(page.getByText(`사용자 '${username}'이(가) 성공적으로 추가되었습니다.`)).toBeVisible();
    
    // Find the row for the new user
    const userRow = page.getByRole('row', { name: new RegExp(username) });
    await expect(userRow).toBeVisible();

    // --- Test Delete Confirmation ---
    
    // 1. Test "Cancel" on delete dialog
    let dialogPromise = page.waitForEvent('dialog');
    await userRow.getByRole('button', { name: '삭제' }).click();
    let dialog = await dialogPromise;
    
    expect(dialog.message()).toBe(`'${username}' 사용자를 정말 삭제할까요?`);
    await dialog.dismiss();
    await expect(userRow).toBeVisible(); // User should still be there

    // 2. Test "OK" on delete dialog
    dialogPromise = page.waitForEvent('dialog');
    await userRow.getByRole('button', { name: '삭제' }).click();
    dialog = await dialogPromise;

    await dialog.accept();
    await expect(page.getByText(`사용자 '${username}'이(가) 삭제되었습니다.`)).toBeVisible();
    await expect(userRow).not.toBeVisible(); // User should be gone

    // --- Test Password Reset Confirmation ---
    
    // Add another user for password reset test
    const pwUsername = rand('pw-testuser');
    await page.locator('#username').fill(pwUsername);
    await page.locator('#password').fill(password);
    await page.getByRole('button', { name: '추가' }).click();
    await expect(page.getByText(`사용자 '${pwUsername}'이(가) 성공적으로 추가되었습니다.`)).toBeVisible();
    const pwUserRow = page.getByRole('row', { name: new RegExp(pwUsername) });

    // Test "OK" on password reset dialog
    dialogPromise = page.waitForEvent('dialog');
    await pwUserRow.getByRole('button', { name: 'PW 초기화' }).click();
    dialog = await dialogPromise;

    expect(dialog.message()).toBe(`'${pwUsername}' 사용자의 비밀번호를 'password'로 초기화할까요?`);
    await dialog.accept();
    await expect(page.getByText(`'${pwUsername}' 사용자의 비밀번호가 'password'(으)로 초기화되었습니다.`)).toBeVisible();
  });
});
