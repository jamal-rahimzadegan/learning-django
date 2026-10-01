import type { ReactNode } from 'react';

interface Props {
  title?: string;
  isLoading?: boolean;
  isEmpty?: boolean;
  children: ReactNode;
}

export default function PageWrapper(props: Props) {
  const { title, isLoading, isEmpty, children } = props;

  if (isLoading) return <b>loading...</b>;

  if (isEmpty) return <b>No data to show</b>;

  return (
    <>
      {title ? (
        <h2 className="font-bold font-stretch-125% mb-5 text-gray-700">
          {title}
        </h2>
      ) : null}
      {children}
    </>
  );
}
