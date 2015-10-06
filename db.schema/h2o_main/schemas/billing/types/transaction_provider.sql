CREATE TYPE billing.transaction_provider AS ENUM ('paypal');
ALTER TYPE billing.transaction_provider ADD VALUE 'stripe';
