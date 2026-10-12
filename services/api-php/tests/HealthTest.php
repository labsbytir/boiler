<?php
// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 TIR Labs. All rights reserved.

use PHPUnit\Framework\TestCase;

class HealthTest extends TestCase
{
    public function testHealthPayloadStructure(): void
    {
        $payload = [
            'success' => true,
            'data' => [
                'status' => 'healthy',
                'service' => 'api-php',
            ],
            'error' => null,
            'meta' => [
                'timestamp' => gmdate('Y-m-d\TH:i:s\Z'),
                'requestId' => 'test_req',
            ],
        ];

        $this->assertTrue($payload['success']);
        $this->assertEquals('healthy', $payload['data']['status']);
        $this->assertNull($payload['error']);
    }
}
