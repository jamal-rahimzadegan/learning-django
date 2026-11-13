import { forwardRef, type ButtonHTMLAttributes } from 'react';
import { twMerge } from 'tailwind-merge';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, type = 'button', children, isLoading, ...restProps }, ref) => {
    const defaultClassName =
      'inline-flex items-center justify-center rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-all duration-150 hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 active:scale-[0.98] disabled:pointer-events-none disabled:opacity-50';

    return (
      <button
        ref={ref}
        type={type}
        className={twMerge(defaultClassName, className)}
        {...restProps}
      >
        {isLoading ? 'loading...' : children}
      </button>
    );
  }
);
