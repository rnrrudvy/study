import { test, expect } from '@playwright/test';

function rand(prefix: string) {
  return prefix + '-' + Math.random().toString(36).slice(2, 8);
}

test('회원가입→로그인→글쓰기→삭제', async ({ page, baseURL }) => {
  const username = rand('user');
  const password = rand('pw');
  const title = rand('title');
  const content = rand('content');

  // 홈
  await page.goto(baseURL!);
  await expect(page.getByText('게시판')).toBeVisible();

  // 회원가입
  await page.getByRole('link', { name: '회원가입' }).click();
  await page.waitForURL('**/register');
  await page.locator('#username').fill(username);
  await page.locator('#password').fill(password);
  await page.getByRole('button', { name: '가입' }).click();

  // 로그인
  await page.locator('#username').fill(username);
  await page.locator('#password').fill(password);
  await page.getByRole('button', { name: '로그인' }).click();
  await expect(page.getByText(`안녕하세요, ${username}님`)).toBeVisible();

  // 글쓰기
  await page.getByRole('link', { name: '글쓰기' }).click();
  await page.getByLabel('제목').fill(title);
  await page.getByLabel('내용').fill(content);
  await page.getByRole('button', { name: '등록' }).click();
  await expect(page.getByText(title)).toBeVisible();

  // 삭제 (첫 글 삭제 버튼 클릭)
  const delButton = page.getByRole('button', { name: '삭제' }).first();
  // confirm 인터셉트
  page.on('dialog', async (dialog) => {
    await dialog.accept();
  });
  await delButton.click();
  await expect(page.getByText(title)).not.toBeVisible();
});

