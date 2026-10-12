<?php
// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 TIR Labs. All rights reserved.

header('Content-Type: application/json; charset=utf-8');

$response = [
    'success' => true,
    'data' => [
        'status' => 'healthy',
        'service' => 'api-php',
        'runtime' => 'php-' . PHP_VERSION,
    ],
    'error' => null,
    'meta' => [
        'timestamp' => gmdate('Y-m-d\TH:i:s\Z'),
        'requestId' => 'req_' . substr(bin2hex(random_bytes(4)), 0, 8),
    ],
];

echo json_encode($response, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
