-- Enable UUID generation
create extension if not exists "pgcrypto";

-- Sellers/leads table
create table if not exists public.sellers (
  id uuid default gen_random_uuid() primary key,
  address text,
  city text,
  zip text,
  owner_name text,
  phone text,
  asking_price numeric,
  arv numeric,
  estimated_repairs numeric,
  offer_price numeric,
  potential_spread numeric,
  equity_percent numeric,
  score integer,
  color text,
  status text default 'new',
  notes text,
  created_at timestamp with time zone default now()
);

-- Buyers table
create table if not exists public.buyers (
  id uuid default gen_random_uuid() primary key,
  name text,
  phone text,
  email text,
  city text,
  zip_codes text,
  max_price numeric,
  notes text,
  created_at timestamp with time zone default now()
);

-- Deals table
create table if not exists public.deals (
  id uuid default gen_random_uuid() primary key,
  seller_id uuid references public.sellers(id) on delete set null,
  contract_price numeric,
  assignment_fee numeric,
  buyer_id uuid references public.buyers(id) on delete set null,
  closing_date date,
  created_at timestamp with time zone default now()
);

create index if not exists sellers_city_idx on public.sellers(city);
create index if not exists sellers_status_idx on public.sellers(status);
create index if not exists sellers_score_idx on public.sellers(score);
create index if not exists buyers_city_idx on public.buyers(city);
