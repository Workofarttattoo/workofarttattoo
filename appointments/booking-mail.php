<?php
/**
 * Work of Art — appointment request → booking@workofarttattoo.com
 * Deploy to /appointments/booking-mail.php on Bluehost (PHP required).
 */
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

const BOOKING_TO = 'booking@workofarttattoo.com';
const BOOKING_FROM = 'noreply@workofarttattoo.com';
const BOOKING_FROM_NAME = 'Work of Art Website';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method not allowed']);
    exit;
}

function clean(string $key, int $max = 2000): string
{
    $raw = $_POST[$key] ?? '';
    if (!is_string($raw)) {
        return '';
    }
    $raw = trim(strip_tags($raw));
    if (strlen($raw) > $max) {
        $raw = substr($raw, 0, $max);
    }
    return $raw;
}

// Honeypot — bots fill this; humans leave empty
if (clean('_woa_hp', 200) !== '') {
    echo json_encode(['ok' => true, 'message' => 'Thank you. We will be in touch shortly.']);
    exit;
}

$service = clean('service_type', 32);
if (!in_array($service, ['tattoo', 'piercing'], true)) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Please choose tattoo or piercing.']);
    exit;
}

$name = clean('full_name', 120);
$email = clean('email', 200);
$phone = clean('phone', 40);

if ($name === '' || $email === '' || $phone === '') {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Name, email, and phone are required.']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Please enter a valid email address.']);
    exit;
}

$ageOk = clean('age_confirm', 8);
if ($ageOk !== 'yes') {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'You must confirm you are 18 or older.']);
    exit;
}

$lines = [
    'New appointment request from workofarttattoo.com',
    '----------------------------------------',
    'Service: ' . strtoupper($service),
    'Name: ' . $name,
    'Email: ' . $email,
    'Phone: ' . $phone,
    'Preferred contact: ' . clean('preferred_contact', 32),
];

if ($service === 'tattoo') {
    $lines[] = 'Request type: ' . clean('tattoo_request_type', 64);
    $lines[] = 'Placement: ' . clean('placement', 200);
    $lines[] = 'Approx. size: ' . clean('tattoo_size', 120);
    $lines[] = 'Preferred artist: ' . clean('preferred_artist', 64);
    $lines[] = 'Timeline: ' . clean('timeline', 200);
    $lines[] = 'Description / idea: ' . clean('description', 4000);
    $lines[] = 'Reference links: ' . clean('reference_links', 2000);
    $subject = '[Tattoo] Appointment request — ' . $name;
} else {
    $lines[] = 'Piercing type: ' . clean('piercing_type', 120);
    $lines[] = 'Jewelry interest: ' . clean('jewelry_interest', 120);
    $lines[] = 'First piercing?: ' . clean('first_piercing', 16);
    $lines[] = 'Preferred piercer: ' . clean('preferred_piercer', 64);
    $lines[] = 'Notes: ' . clean('piercing_notes', 4000);
    $subject = '[Piercing] Appointment request — ' . $name;
}

$lines[] = '----------------------------------------';
$lines[] = 'Submitted: ' . gmdate('Y-m-d H:i:s') . ' UTC';
$lines[] = 'IP: ' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown');

$body = implode("\n", $lines) . "\n";
$fromHeader = 'From: ' . BOOKING_FROM_NAME . ' <' . BOOKING_FROM . '>';
$replyHeader = 'Reply-To: ' . $name . ' <' . $email . '>';
$headers = implode("\r\n", [
    $fromHeader,
    $replyHeader,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion(),
]);

$ok = @mail(BOOKING_TO, $subject, $body, $headers);

if (!$ok) {
    http_response_code(500);
    echo json_encode([
        'ok' => false,
        'error' => 'Could not send email from the server. Please call (725) 224-1240 or email booking@workofarttattoo.com directly.',
        'fallback' => true,
    ]);
    exit;
}

echo json_encode([
    'ok' => true,
    'message' => 'Thank you — your request was sent to our booking team. We typically reply within one business day.',
]);
