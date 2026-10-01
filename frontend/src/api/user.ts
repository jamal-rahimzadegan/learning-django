import { apiSvc } from '../svc/api-svc.ts';

interface User {}

interface LoginRes {
  access: string;
  refresh: string;
}

async function login(paylod: {
  username: string;
  password: string;
}): Promise<boolean> {
  try {
    const res = await apiSvc.post<LoginRes>('/accounts/login', {
      ...paylod,
    });
    setTokens(res.access, res.refresh);
    return true;
  } catch (e) {
    return false;
  }
}

async function refreshToken() {
  const refreshToken = localStorage.getItem('refreshToken');

  if (!refreshToken) return;

  const res = await apiSvc.post<unknown>('/accounts/refresh', {
    refresh: refreshToken,
  });
  //   TODO: implement
}

function setTokens(token: string, refreshToken: string) {
  localStorage.setItem('token', token);
  localStorage.setItem('refreshToken', refreshToken);
}

function checkIsLoggedIn() {
  return localStorage.getItem('token');
}

export type { User };

export { login, refreshToken, checkIsLoggedIn };
