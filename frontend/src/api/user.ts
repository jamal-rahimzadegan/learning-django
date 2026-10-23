import { apiSvc } from '../svc/api-svc.ts';

interface User {}

interface TokenRes {
  access: string;
  refresh: string;
}

async function login(paylod: {
  username: string;
  password: string;
}): Promise<boolean> {
  try {
    const res = await apiSvc.post<TokenRes>('/accounts/login', {
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

  await apiSvc
    .post<TokenRes>('/accounts/refresh', {
      refresh: refreshToken,
    })
    .then((data) => setTokens(data.access, data.refresh))
    .catch((err) => {
      console.log(err);
    });
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
