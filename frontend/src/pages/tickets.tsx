import PageWrapper from '../layout/page-wrapper.tsx';
import { useQuery } from '@tanstack/react-query';
import { getTickets } from '../api/tickets.ts';

export default function Tickets() {
  const { data: tickets = [], isFetching } = useQuery({
    queryKey: ['tickets'],
    queryFn: () => getTickets(),
  });

  return (
    <PageWrapper
      title="My Tickets"
      isEmpty={!tickets?.length}
      isLoading={isFetching}
    >
      {tickets?.map((ticket, i) => (
        <h3 className="font-bold">
          {i + 1}- {ticket.status}
        </h3>
      ))}
    </PageWrapper>
  );
}
