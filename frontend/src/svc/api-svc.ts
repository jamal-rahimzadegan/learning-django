import { refreshToken } from '../api/user.ts';

interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown;
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
const API_VERSION = import.meta.env.VITE_API_VERSION || '';

async function createRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { body, headers, ...customConfig } = options;
  const token = localStorage.getItem('token');
  const tokenRefresh = localStorage.getItem('refreshToken');

  const config: RequestInit = {
    method: options.method || 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...headers,
    },
    ...(body !== undefined && { body: JSON.stringify(body) }),
    ...customConfig,
  };

  const version = endpoint.includes('accounts') ? '' : `/${API_VERSION}`;

  let response = await fetch(`${BASE_URL}${version}${endpoint}`, config);

  if (response.status === 401 && tokenRefresh) await refreshToken();

  if (response.status === 204) return {} as T;

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const errorMsg =
      data?.detail ||
      data?.message ||
      `HTTP ${response.status}: ${response.statusText}`;
    throw new Error(errorMsg);
  }

  return data as T;
}

export const apiSvc = {
  get: <T>(endpoint: string, options?: RequestOptions) =>
    createRequest<T>(endpoint, { ...options, method: 'GET' }),

  post: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    createRequest<T>(endpoint, { ...options, method: 'POST', body }),

  put: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    createRequest<T>(endpoint, { ...options, method: 'PUT', body }),

  patch: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    createRequest<T>(endpoint, { ...options, method: 'PATCH', body }),

  delete: <T>(endpoint: string, options?: RequestOptions) =>
    createRequest<T>(endpoint, { ...options, method: 'DELETE' }),
};
