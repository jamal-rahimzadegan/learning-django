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

    localStorage.setItem('token', res.access);
    localStorage.setItem('refreshToken', res.refresh);
    return true;
  } catch (e) {
    return false;
  }
}

async function refreshToken() {
  const refreshToken = localStorage.getItem('refreshToken');
  return await apiSvc.post<unknown>('/accounts/refresh', {
    refresh: refreshToken,
  });
}

function checkIsLoggedIn() {
  return localStorage.getItem('token');
}

export type { User };

export { login, refreshToken, checkIsLoggedIn };
