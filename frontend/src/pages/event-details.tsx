import { getEvents, type SocialEvent } from '../api/events.ts';
import { useParams } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import PageWrapper from '../layout/page-wrapper.tsx';
import { Button } from '../components/shared/button.tsx';
import { handleCheckout } from '../api/payment.ts';

export default function EventDetails() {
  const { id } = useParams();

  const { data: event, isFetching } = useQuery({
    enabled: !!id,
    queryKey: ['event', id],
    queryFn: () => getEvents<SocialEvent>(id),
  });

  const { isPending, mutateAsync: mutateCheckout } = useMutation({
    mutationFn: handleCheckout,
    onSuccess: (res) => {
      console.log('res: ', res);
      return (window.location.href = res?.url);
    },
  });

  const price = event?.price || 0;

  return (
    <PageWrapper isEmpty={!event?.id} isLoading={isFetching}>
      <div key={event?.id} className="mb-3">
        <h3 className="font-bold mt-5">{event?.title}</h3>
        <p className="mt-2">{event?.description}</p>
      </div>
      {price > 0 ? (
        <Button
          onClick={() => mutateCheckout(event?.id || '')}
          isLoading={isPending}
        >
          Buy {price} €
        </Button>
      ) : null}
    </PageWrapper>
  );
}
