FROM node:18-alpine

# Install aws-cost-cli globally
RUN npm install -g aws-cost-cli

# Set working directory
WORKDIR /app

# Default command
CMD ["aws-cost"]
