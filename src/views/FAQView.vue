<script setup>
import { ref } from "vue";

const faqs = ref([
  {
    id: 1,
    question: "What is InsideView?",
    answer:
      "InsideView is a comprehensive platform that provides access to urban data, analytics, and reporting tools. Our mission is to empower users with the insights they need to make informed decisions about urban environments. We offer a wide range of datasets, from real estate and demographics to transportation and environmental quality, all presented in an intuitive and accessible interface.",
  },
  {
    id: 2,
    question: "What are the data sources for InsideView?",
    answer:
      "InsideView aggregates data from multiple reliable open data sources, public APIs, and verified partners. These include municipal databases, tourism agencies, and third-party analytics providers to ensure both accuracy and up-to-date information.",
  },
  {
    id: 3,
    question: "How often is the data updated?",
    answer:
      "Our data is updated regularly depending on the source: Public datasets are refreshed monthly or quarterly. Private or API-based data may update daily or weekly. All updates are automatically reflected in charts, filters, and reports.",
  },
  {
    id: 4,
    question: "How can I export a report?",
    answer:
      "You can generate and export reports directly from the Export Data page. Select your filters (city, neighborhood, property type, etc.), choose your file format (PDF, CSV, JSON), and click Generate Report. The system will automatically generate a summary with your active filters.",
  },
  {
    id: 6,
    question: "Can I create customized reports?",
    answer:
      "Yes. You can combine filters, select specific data categories, and export your report in different formats. This allows you to generate insights tailored to your needs, whether for market research, academic analysis, or bu...",
  },
  // Add more if needed
]);

const openFaqId = ref(null);

function toggleFaq(id) {
  openFaqId.value = openFaqId.value === id ? null : id;
}
</script>

<template>
  <div class="faq-page">
    <h1>Frequently Asked Questions</h1>
    <div class="faq-list">
      <div
        v-for="faq in faqs"
        :key="faq.id"
        class="faq-item"
        :class="{ open: openFaqId === faq.id }"
      >
        <div class="faq-question" @click="toggleFaq(faq.id)">
          {{ faq.question }}
          <div class="chevron-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
            >
              <path
                fill="none"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2.5"
                d="m6 9l6 6l6-6"
              />
            </svg>
          </div>
        </div>

        <div class="faq-answer">
          <div class="faq-answer-content">
            {{ faq.answer }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.faq-page {
  width: 100%;
  padding: 2rem 1rem;
  max-width: 1000px;
  color: black;
}

.faq-page h1 {
  font-weight: 800;
  font-size: 2rem;
  margin: 0 0 1.5rem 0;
  color: black;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  transition: all 0.3s ease;
}

.faq-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  font-weight: 600;
  color: black;
  cursor: pointer;
  user-select: none;
  background: white;
}

.chevron-icon {
  color: #ff5a5f;
  transition: transform 0.3s ease;
  min-width: 20px;
}

.faq-item.open .chevron-icon {
  transform: rotate(180deg);
}

.faq-answer {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s ease-out, border-top 0.3s ease;
}

.faq-item.open .faq-answer {
  grid-template-rows: 1fr;
  border-top: 1px solid lightgrey;
}

.faq-answer-content {
  min-height: 0;
  overflow: hidden;
  color: dimgrey;
  line-height: 1.6;
  font-size: 0.95rem;
  padding: 0;
  opacity: 0;
  transition: opacity 0.3s ease, padding 0.3s ease;
}

.faq-item.open .faq-answer-content {
  padding: 0.5rem 1rem;
  opacity: 1;
}
</style>
