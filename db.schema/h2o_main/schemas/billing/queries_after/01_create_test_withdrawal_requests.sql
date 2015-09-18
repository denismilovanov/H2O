INSERT INTO billing.withdrawal_requests
    (id, user_id, user_uuid, amount, currency, provider, provider_transaction_id, email)
    VALUES
    (
        -1,
        -1,
        (SELECT uuid FROM main.users WHERE id = -1),
        77,
        'usd',
        'paypal',
        '123456789012',
        'denis.s.milovanov@gmail.com'
    );
