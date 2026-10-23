import { getEvents, type SocialEvent } from '../api/events.ts';
import { Link } from 'react-router-dom';
import PageWrapper from '../layout/page-wrapper.tsx';
import { useQuery } from '@tanstack/react-query';

export default function Home() {
  const { data: events = [], isFetching } = useQuery({
    queryKey: ['events'],
    queryFn: () => getEvents<SocialEvent[]>(),
  });

  return (
    <PageWrapper
      title="Events List"
      isEmpty={!events?.length}
      isLoading={isFetching}
    >
      {events?.map((event, i) => (
        <Link
          to={`/event/${event.id}`}
          key={event.id}
          className="mb-3 block cursor-pointer"
        >
          <h3 className="font-bold">
            {i + 1}- {event.title}
          </h3>
        </Link>
      ))}
    </PageWrapper>
  );
}
