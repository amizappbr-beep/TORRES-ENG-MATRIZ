// Feirão do Imóvel — Torres Engenharia
// Conteúdo configurável do frontend (imagens, textos, quiz).
// Estoque, preços e condições vêm do backend (/api/feirao/config) e do admin.

export const IMAGES = {
  hero: "https://images.unsplash.com/photo-1515263487990-61b07816b324?crop=entropy&cs=srgb&fm=jpg&q=85&w=1600",
  casaPronta:
    "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200",
  familia:
    "https://images.unsplash.com/photo-1709787627975-9cb37bbeca60?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200",
  quintal:
    "https://images.pexels.com/photos/7061676/pexels-photo-7061676.jpeg?auto=compress&cs=tinysrgb&w=1200",
};

// Conteúdo estático por empreendimento (galeria + argumentos).
// Estoque/preço/entrada são sobrescritos pelo config do backend.
export const EMPREENDIMENTOS = {
  viva: {
    slug: "viva",
    nome: "Residencial Viva",
    regiao: "Jacaraípe",
    tagline: "Casas duplex a poucos minutos da praia.",
    cover: "/viva-fachada.jpg",
    galeria: [
      "/viva-fachada.jpg",
      "/viva-int-1.jpg",
      "/viva-int-2.webp",
    ],
    beneficios: [
      "Jacaraípe, com a praia por perto",
      "Casas duplex de 2 a 3 quartos com suíte",
      "Quintal / garden",
      "Perfil familiar e qualidade de vida",
    ],
    descricao:
      "O Residencial Viva reúne casas duplex em Jacaraípe, ideais para quem busca proximidade da praia, quintal e espaço para a família. Enquadramento em financiamento habitacional conforme análise individual.",
  },
  alameda: {
    slug: "alameda",
    nome: "Alameda",
    regiao: "Serra",
    tagline: "Oportunidade prioritária do Feirão. Estoque reduzido.",
    cover: "/alameda-fachada.jpg",
    galeria: [
      "/alameda-fachada.jpg",
      "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200",
      "https://images.pexels.com/photos/6980724/pexels-photo-6980724.jpeg?auto=compress&cs=tinysrgb&w=1200",
    ],
    beneficios: [
      "Localização na Serra",
      "Produto familiar",
      "Condições comerciais do Feirão",
      "Estoque reduzido — oportunidade real",
    ],
    descricao:
      "O Alameda é o empreendimento prioritário desta campanha, com estoque reduzido e condições especiais no Feirão. Possibilidade de análise de financiamento conforme perfil.",
  },
  life: {
    slug: "life",
    nome: "Residencial Life",
    regiao: "Serra",
    tagline: "Última unidade disponível.",
    cover: "/life-fachada.jpg",
    video: "/life.mp4",
    galeria: [
      "/life-fachada.jpg",
      "https://images.pexels.com/photos/29012619/pexels-photo-29012619.jpeg?auto=compress&cs=tinysrgb&w=1200",
    ],
    beneficios: ["Última unidade", "Pronta para morar", "Localização na Serra"],
    descricao:
      "O Residencial Life está na sua última unidade. Uma oportunidade real de garantir uma casa Torres pronta.",
  },
  aldeia: {
    slug: "aldeia",
    nome: "Residencial Aldeia",
    regiao: "Serra",
    tagline: "Última unidade disponível.",
    cover: "/aldeia-fachada.jpg",
    galeria: [
      "/aldeia-fachada.jpg",
      "https://images.unsplash.com/photo-1709787627975-9cb37bbeca60?crop=entropy&cs=srgb&fm=jpg&q=85&w=1200",
    ],
    beneficios: [
      "Última unidade",
      "Empreendimento já entregue e habitado",
      "Perfil familiar",
    ],
    descricao:
      "O Residencial Aldeia está na sua última unidade, em um empreendimento já entregue e habitado — prova do padrão Torres Engenharia.",
  },
};

// ---- Quiz de pré-qualificação (12 perguntas) ----
// type: 'single' | 'multi'. follow: pergunta condicional exibida quando
// a resposta pertence a `when`.
export const QUIZ = [
  {
    id: "objetivo",
    type: "single",
    titulo: "O que você procura hoje?",
    opcoes: [
      { value: "primeira_casa", label: "Comprar minha primeira casa" },
      { value: "sair_aluguel", label: "Sair do aluguel" },
      { value: "casa_maior", label: "Comprar uma casa maior" },
      { value: "investir", label: "Investir em imóvel" },
      { value: "pesquisando", label: "Estou apenas pesquisando" },
    ],
  },
  {
    id: "prazo",
    type: "single",
    titulo: "Quando você pretende comprar?",
    opcoes: [
      { value: "imediato", label: "Imediatamente" },
      { value: "30d", label: "Nos próximos 30 dias" },
      { value: "1_3m", label: "Entre 1 e 3 meses" },
      { value: "3_6m", label: "Entre 3 e 6 meses" },
      { value: "nao_sei", label: "Ainda não sei" },
    ],
  },
  {
    id: "renda_familiar",
    type: "single",
    titulo: "Qual é aproximadamente a renda mensal da sua família?",
    ajuda:
      "Essa informação ajuda a identificar as opções de financiamento mais adequadas.",
    opcoes: [
      { value: "ate_3k", label: "Até R$ 3.000" },
      { value: "3_4.5k", label: "R$ 3.001 a R$ 4.500" },
      { value: "4.5_6k", label: "R$ 4.501 a R$ 6.000" },
      { value: "6_8k", label: "R$ 6.001 a R$ 8.000" },
      { value: "8_12k", label: "R$ 8.001 a R$ 12.000" },
      { value: "acima_12k", label: "Acima de R$ 12.000" },
    ],
  },
  {
    id: "composicao_renda",
    type: "single",
    titulo: "Você compraria sozinho ou poderia compor renda com outra pessoa?",
    opcoes: [
      { value: "sozinho", label: "Sozinho" },
      { value: "conjuge", label: "Cônjuge / companheiro(a)" },
      { value: "familiar", label: "Familiar" },
      { value: "nao_sei", label: "Ainda não sei" },
    ],
  },
  {
    id: "tipo_renda",
    type: "multi",
    max: 3,
    titulo: "Como você comprova sua renda hoje?",
    ajuda: "Pode escolher mais de uma opção.",
    opcoes: [
      { value: "clt", label: "Carteira assinada / CLT" },
      { value: "servidor", label: "Servidor público" },
      { value: "empresario", label: "Empresário" },
      { value: "mei", label: "MEI" },
      { value: "autonomo", label: "Autônomo" },
      { value: "aposentado", label: "Aposentado" },
      { value: "outro", label: "Outro" },
    ],
  },
  {
    id: "fgts",
    type: "single",
    titulo: "Você possui FGTS disponível?",
    opcoes: [
      { value: "sim", label: "Sim" },
      { value: "nao", label: "Não" },
      { value: "nao_sei", label: "Não sei quanto tenho" },
    ],
    follow: {
      when: ["sim"],
      id: "fgts_valor",
      type: "single",
      titulo: "Qual o valor aproximado do seu FGTS?",
      opcoes: [
        { value: "ate_10k", label: "Até R$ 10 mil" },
        { value: "10_30k", label: "R$ 10 mil a R$ 30 mil" },
        { value: "30_50k", label: "R$ 30 mil a R$ 50 mil" },
        { value: "mais_50k", label: "Mais de R$ 50 mil" },
        { value: "nao_sei", label: "Não sei" },
      ],
    },
  },
  {
    id: "entrada",
    type: "single",
    titulo:
      "Hoje, aproximadamente quanto você conseguiria usar como entrada na compra?",
    opcoes: [
      { value: "sem_entrada", label: "Ainda não tenho entrada" },
      { value: "ate_10k", label: "Até R$ 10 mil" },
      { value: "10_30k", label: "R$ 10 mil a R$ 30 mil" },
      { value: "30_50k", label: "R$ 30 mil a R$ 50 mil" },
      { value: "50_100k", label: "R$ 50 mil a R$ 100 mil" },
      { value: "100_150k", label: "R$ 100 mil a R$ 150 mil" },
      { value: "acima_150k", label: "Acima de R$ 150 mil" },
    ],
  },
  {
    id: "moradia",
    type: "single",
    titulo: "Hoje você:",
    opcoes: [
      { value: "aluguel", label: "Mora de aluguel" },
      { value: "familiares", label: "Mora com familiares" },
      { value: "proprio", label: "Já possui imóvel próprio" },
      { value: "financiado", label: "Possui imóvel financiado" },
      { value: "outro", label: "Outro" },
    ],
    follow: {
      when: ["aluguel"],
      id: "aluguel_valor",
      type: "single",
      titulo: "Quanto aproximadamente você paga de aluguel?",
      opcoes: [
        { value: "ate_800", label: "Até R$ 800" },
        { value: "800_1200", label: "R$ 800 a R$ 1.200" },
        { value: "1200_1800", label: "R$ 1.200 a R$ 1.800" },
        { value: "acima_1800", label: "Acima de R$ 1.800" },
      ],
    },
  },
  {
    id: "financiamento",
    type: "single",
    titulo: "Você já fez alguma simulação de financiamento recentemente?",
    opcoes: [
      { value: "aprovado", label: "Sim, e fui aprovado" },
      { value: "nao_aprovado", label: "Sim, mas não fui aprovado" },
      { value: "nao_conclui", label: "Fiz simulação, mas não concluí" },
      { value: "nunca", label: "Nunca fiz" },
    ],
    follow: {
      when: ["aprovado"],
      id: "financiamento_valor",
      type: "single",
      titulo: "Qual valor foi aprovado (aproximadamente)?",
      opcoes: [
        { value: "ate_150k", label: "Até R$ 150 mil" },
        { value: "150_250k", label: "R$ 150 mil a R$ 250 mil" },
        { value: "250_400k", label: "R$ 250 mil a R$ 400 mil" },
        { value: "acima_400k", label: "Acima de R$ 400 mil" },
      ],
    },
  },
  {
    id: "restricao",
    type: "single",
    titulo:
      "Existe hoje alguma situação que possa dificultar uma análise de crédito?",
    ajuda: "Fique tranquilo — isso não impede a sua participação no Feirão.",
    opcoes: [
      { value: "nao", label: "Não" },
      { value: "sim", label: "Sim" },
      { value: "nao_certeza", label: "Não tenho certeza" },
    ],
  },
  {
    id: "regiao",
    type: "single",
    titulo: "Qual região mais interessa para você?",
    opcoes: [
      { value: "jacaraipe", label: "Jacaraípe" },
      { value: "alterosas", label: "Alterosas" },
      { value: "serra", label: "Serra" },
      { value: "aberto", label: "Estou aberto a diferentes regiões" },
      { value: "todas", label: "Quero conhecer todas as oportunidades" },
    ],
  },
  {
    id: "preferencias",
    type: "multi",
    max: 3,
    titulo: "O que é mais importante na sua próxima casa?",
    ajuda: "Escolha até 3.",
    opcoes: [
      { value: "preco", label: "Preço" },
      { value: "entrada_facil", label: "Entrada facilitada" },
      { value: "localizacao", label: "Localização" },
      { value: "praia", label: "Proximidade da praia" },
      { value: "quintal", label: "Quintal" },
      { value: "duplex", label: "Casa duplex" },
      { value: "ultima_unidade", label: "Última unidade / oportunidade" },
      { value: "valorizacao", label: "Potencial de valorização" },
    ],
  },
];

export const HORARIOS = [
  { value: "manha", label: "Manhã" },
  { value: "inicio_tarde", label: "Início da tarde" },
  { value: "final_tarde", label: "Final da tarde" },
];

export function buildWhatsappUrl({ phone, empreendimentoNome, leadId }) {
  const code = leadId ? ` (código ${leadId.slice(0, 8).toUpperCase()})` : "";
  const emp = empreendimentoNome ? ` no ${empreendimentoNome}` : "";
  const msg = `Olá! Acabei de fazer a análise no site do Feirão Torres Engenharia. Tenho interesse${emp} e gostaria de entender melhor as condições.${code}`;
  return `https://wa.me/${phone}?text=${encodeURIComponent(msg)}`;
}
