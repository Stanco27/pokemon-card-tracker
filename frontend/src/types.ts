export interface SniperConfig {
  tcin: string;
  interval: number;
  session_id: string;
  auto_checkout: boolean;
}

export type ViewState = 'home' | 'dashboard';