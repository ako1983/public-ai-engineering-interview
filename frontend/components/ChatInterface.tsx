import { 
  VStack, 
  HStack, 
  Heading, 
  Text, 
  Input, 
  Button, 
  Box,
  InputGroup,
  InputRightElement,
  Spinner,
  Alert,
  AlertIcon
} from "@chakra-ui/react";
import { Card } from "./Card";
import { useState } from "react";
import { Client } from "../lib/client";

interface ChatMessage {
  id: string;
  message: string;
  response: string;
  timestamp: Date;
  isLoading?: boolean;
}

export const ChatInterface = ({ userId }: { userId: string | null }) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!message.trim() || !userId) return;

    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      message: message.trim(),
      response: "",
      timestamp: new Date(),
      isLoading: true
    };

    setMessages(prev => [...prev, newMessage]);
    setMessage("");
    setIsLoading(true);

    try {
      const client = new Client();
      const response = await client.sendChatMessage(userId, message.trim());
      
      setMessages(prev => 
        prev.map(msg => 
          msg.id === newMessage.id 
            ? { ...msg, response: response.message, isLoading: false }
            : msg
        )
      );
    } catch (error) {
      setMessages(prev => 
        prev.map(msg => 
          msg.id === newMessage.id 
            ? { ...msg, response: "Sorry, I encountered an error processing your request.", isLoading: false }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Card>
      <Heading size={"md"}>2. Chat with your AI Health Assistant</Heading>
      <Text>
        Ask questions about your health data, request prescription refills, book appointments, 
        or get insights about your chronic conditions and biometric trends.
      </Text>
      
      {!userId && (
        <Alert status="warning" borderRadius="md">
          <AlertIcon />
          Please select a user above to start chatting.
        </Alert>
      )}

      {userId && (
        <VStack width="100%" spacing={4} alignItems="flex-start">
          {/* Chat Messages */}
          <Box 
            width="100%" 
            maxHeight="400px" 
            overflowY="auto" 
            border="1px solid #e3ebf6" 
            borderRadius="md" 
            p={4}
            backgroundColor="#fafafa"
          >
            {messages.length === 0 && (
              <Text color="gray.500" fontSize="sm" textAlign="center">
                No messages yet. Try asking: "How are my glucose levels?" or "Can you refill my diabetes medication?"
              </Text>
            )}
            
            <VStack spacing={4} alignItems="flex-start">
              {messages.map((msg) => (
                <Box key={msg.id} width="100%">
                  {/* User Message */}
                  <Box 
                    backgroundColor="blue.50" 
                    p={3} 
                    borderRadius="md" 
                    borderLeftWidth="4px" 
                    borderLeftColor="blue.400"
                  >
                    <Text fontSize="sm" fontWeight="medium" color="blue.800">
                      You:
                    </Text>
                    <Text fontSize="sm">{msg.message}</Text>
                  </Box>
                  
                  {/* AI Response */}
                  <Box 
                    mt={2} 
                    backgroundColor="green.50" 
                    p={3} 
                    borderRadius="md"
                    borderLeftWidth="4px" 
                    borderLeftColor="green.400"
                  >
                    <Text fontSize="sm" fontWeight="medium" color="green.800">
                      AI Assistant:
                    </Text>
                    {msg.isLoading ? (
                      <HStack>
                        <Spinner size="sm" />
                        <Text fontSize="sm" color="gray.600">Thinking...</Text>
                      </HStack>
                    ) : (
                      <Text fontSize="sm" whiteSpace="pre-wrap">{msg.response}</Text>
                    )}
                  </Box>
                </Box>
              ))}
            </VStack>
          </Box>

          {/* Input Area */}
          <InputGroup size="md" width="100%">
            <Input
              placeholder="Ask about your health data, request prescription refills, book appointments..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={!userId || isLoading}
              pr="4.5rem"
            />
            <InputRightElement width="4.5rem">
              <Button
                h="1.75rem"
                size="xs"
                onClick={handleSendMessage}
                isLoading={isLoading}
                disabled={!userId || !message.trim()}
                colorScheme="blue"
              >
                Send
              </Button>
            </InputRightElement>
          </InputGroup>

          {/* Example Questions */}
          <Box width="100%">
            <Text fontSize="sm" fontWeight="medium" mb={2}>
              Try these example questions:
            </Text>
            <VStack spacing={1} alignItems="flex-start">
              {[
                "How are my glucose levels trending this week?",
                "How are my heartrate levels trending this week?",
                "What chronic conditions should I monitor?",
                "What recent vital events should I be aware of?"
              ].map((example, index) => (
                <Button
                  key={index}
                  variant="ghost"
                  size="xs"
                  fontSize="xs"
                  color="blue.600"
                  onClick={() => setMessage(example)}
                  disabled={!userId || isLoading}
                >
                  "{example}"
                </Button>
              ))}
            </VStack>
          </Box>
        </VStack>
      )}
    </Card>
  );
};