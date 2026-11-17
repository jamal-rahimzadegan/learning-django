import { apiSvc } from '../svc/api-svc.ts';

async function getTickets(): Promise<unknown> {
  return await apiSvc.get<unknown[]>(`/tickets`);
}

export { getTickets };
