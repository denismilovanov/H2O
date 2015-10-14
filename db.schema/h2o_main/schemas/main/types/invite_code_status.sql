CREATE TYPE main.invite_code_status AS ENUM ('free', 'sending', 'awaiting_registration', 'used');

ALTER TYPE main.invite_code_status ADD VALUE 'ios_build_requested';
